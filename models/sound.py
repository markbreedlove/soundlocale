# Copyright (C) 2013  Mark Breedlove
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
                  'user_id': str(self.user.id), 'looping': self.flags & LOOPING,
                  'created': self.created, 'modified': self.modified}
        if hasattr(self, 'distance'):
            result['distance'] = self.distance
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


def sounds_near(lat, lng, meters, storage_config):
    b = boundaries(lat, lng, meters)
    q = Sound.select() \
             .where(Sound.lat.between(b['n'], b['s'])) \
             .where(Sound.lng.between(b['w'], b['e']))
    near_sounds = filtered_by_radius(q, lat, lng, meters)
    return [s.for_api(storage_config) for s in near_sounds]

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

