
import peewee
from simpleflake import simpleflake
from util import boundaries, distance
from base import BaseModel
from user import User
from checks import *

class Sound(BaseModel):
    id = peewee.BigIntegerField(primary_key=True)
    lat = peewee.DoubleField()
    lng = peewee.DoubleField()
    basename = peewee.CharField()
    title = peewee.CharField()
    container = peewee.CharField()
    user = peewee.ForeignKeyField(User, related_name='sounds')

    def for_api(self, storage_config):
        """
        Return a dictionary of the current record, suitable for API output,
        where the URL is given.
        """
        base_url = storage_config[self.container]['base_url']
        if not base_url.endswith('/'):
            base_url += '/'
        result = {'id': self.id, 'lat': self.lat, 'lng': self.lng,
                  'url': base_url + self.basename, 'title': self.title,
                  'user_id': self.user.id}
        if hasattr(self, 'distance'):
            result['distance'] = self.distance
        return result


def add_sound(lat, lng, basename, title, container, user):
    return Sound.create(id=simpleflake(),
                        lat=check_float(lat),
                        lng=check_float(lng),
                        basename=check_notempty(basename),
                        title=title,
                        container=check_notempty(container),
                        user=user)

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

