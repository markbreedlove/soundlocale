# Copyright (C) Mark Breedlove and Qingyang Xi
# See README.md and License.txt.

"""
Sound peewee model and sound file-related functions
"""

import peewee
from time import time
from simpleflake import simpleflake
from util import boundaries, distance
from base import BaseModel
from user import User
from checks import *
from ourcrypto import unsign
from ourexceptions import *

LOOPING = 1 << 0
MP3     = 1 << 5
M4A     = 1 << 6
OGG     = 1 << 7


class Sound(BaseModel):
    id = peewee.BigIntegerField(primary_key=True)
    lat = peewee.DoubleField()
    lng = peewee.DoubleField()
    basename = peewee.CharField()
    title = peewee.CharField()
    container = peewee.CharField()
    user = peewee.ForeignKeyField(User, related_name='sounds')
    flags = peewee.IntegerField()
    created = peewee.IntegerField()
    modified = peewee.IntegerField()

    def save(self, *args, **kwargs):
        self.modified = int(time())
        return super(Sound, self).save(*args, **kwargs)

    def for_api(self, storage_config):
        """
        Return a dictionary of the current record, suitable for API output,
        where the URL is given.
        """
        base_url = storage_config[self.container]['base_url']
        if not base_url.endswith('/'):
            base_url += '/'
        result = {'id': str(self.id), 'lat': self.lat, 'lng': self.lng,
                  'url': base_url + self.basename, 'title': self.title,
                  'user_id': str(self.user.id),
                  'looping': int(self.flags & LOOPING > 0),
                  'mp3': int(self.flags & MP3 > 0),
                  'm4a': int(self.flags & M4A > 0),
                  'ogg': int(self.flags & OGG > 0),
                  'created': self.created,
                  'modified': self.modified}
        if hasattr(self, 'distance'):
            result['distance'] = self.distance
        if hasattr(self, 'program'):
            result['program'] = self.program
        else:
            result['program'] = {'id': str(self.user.id),
                                 'name': self.user.fullname,
                                 'token': "u%s" % self.user.id}
        return result


def add_sound(lat, lng, basename, title, container, user, flags):
    timestamp = int(time())
    return Sound.create(id=simpleflake(),
                        lat=check_float(lat),
                        lng=check_float(lng),
                        basename=check_notempty(basename),
                        title=title,
                        container=check_notempty(container),
                        user=user,
                        flags=flags,
                        created=timestamp,
                        modified=timestamp)


def sounds_near(lat, lng, meters, storage_config, user_id=None, for_api=True):
    b = boundaries(lat, lng, meters)
    q = peewee.SelectQuery(Sound) \
             .where(Sound.lat.between(b['n'], b['s'])) \
             .where(Sound.lng.between(b['w'], b['e']))
    if user_id:
        q = q.join(User).where(User.id == user_id)
    near_sounds = filtered_by_radius(q, lat, lng, meters)
    if for_api:
        return [s.for_api(storage_config) for s in near_sounds]
    else:
        return near_sounds

def filtered_by_radius(sounds, lat, lng, meters):
    '''
    Given a list of sounds, a pair of coordinates representing a center point,
    and a radius in meters from the center point, yield an iterator that
    gives the elements of the original list that are within the radius.
    '''
    for s in sounds:
        d = distance(lat, lng, s.lat, s.lng)
        if d < meters:
            s.distance = d
            yield s

def get_with_auth_token(id, auth_token, config):
    """Return one sound matching the given parameters"""
    token = unsign(auth_token, config)
    return Sound.select() \
                .join(User) \
                .where((Sound.id == id) &
                       (User.auth_token == token)) \
                .get()

def get_all_for_auth_token(auth_token, config):
    """Return all of the sounds for a user, for API output"""
    token = unsign(auth_token, config)
    sounds = Sound.select().join(User).where(User.auth_token == token)
    return [s.for_api(config['STORAGE']) for s in sounds]

