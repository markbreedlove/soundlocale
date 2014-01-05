# Copyright (C) 2013  Mark Breedlove and Qingyang Xi
# See README.md and License.txt.

"""
Program-related view functions
"""

__all__ = ['programs_near']

from flask import jsonify, request
import models.sound as sound
from app import app
from ourexceptions import *


@app.route('/programs/near/<float:lat>,<float:lng>,<int:meters>.json')
def programs_near(lat, lng, meters):
    """
    Retrieve programs containing sounds near the given coordinates, within
    the given distance in meters.
    """
    sounds = sound.sounds_near(lat=lat, lng=lng, meters=meters,
                               storage_config=app.config['STORAGE'],
                               for_api=False)
    programs = {}
    for s in sounds:
        p = _program_for_sound(s)
        if p['id'] not in programs:
            programs[p['id']] = p
    return jsonify({'programs': programs.values()})

def _program_for_sound(sound):
    if hasattr(sound, 'program'):
        return {'id': sound.program.id, 'token': 'p%s' % sound.program.id,
                'name': sound.program.name}
    else:
        return {'id': sound.user.id, 'token': 'u%s' % sound.user.id,
                'name': sound.user.fullname}

