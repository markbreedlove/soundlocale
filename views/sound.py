# Copyright (C) 2013  Mark Breedlove
# See README.md and License.txt.

"""
Sound file-related view functions
"""

__all__ = ['add_sound', 'view_sound', 'delete_sound', 'edit_sound',
           'sounds_near']

from flask import jsonify, request
from os import unlink
import simpleflake
import mimetypes
import re
import models.sound as sound
import models.user as user
from util import form_or_json
from app import app
from werkzeug import secure_filename
from exceptions import KeyError, ValueError
from ourexceptions import *


@app.route('/sounds.json', methods=['POST'])
def add_sound():
    """
    API:  Add a sound file

    Querystring parameters:  auth_token
    POST data: lat, lng, title, looping, soundfile

    Returns ID of newly-created sound resource, as: {"id": <the id>}
    """
    try:
        u = user.get(auth_token=request.args.get('auth_token'),
                     config=app.config)
        data = form_or_json()
        lat = float(data['lat'])
        lng = float(data['lng'])
        title = data['title'].strip()
        looping = ('looping' in data)
        flags = 0
        flags |= (looping and sound.LOOPING)
        container = 'container_1'
        file = request.files['soundfile']
        check_filetype(file.filename)
        file_name = unique_filename(file.filename)
        file.save(app.config['STORAGE'][container]['fs_path'] + file_name)
        new_sound = sound.add_sound(lat=lat, lng=lng, title=title,
                                    basename=file_name, container=container,
                                    user=u, flags=flags)
        return jsonify(new_sound.for_api(app.config['STORAGE']))
    except user.User.DoesNotExist:
        response = jsonify(message='Unauthorized')
        response.status_code = 401
        return response
    except (ValueError, BadRequestError):
        response = jsonify(message='Bad Request')
        response.status_code = 400
        return response

def check_filetype(filename):
    t = mimetypes.guess_type(filename)
    if t and t[0] in ('audio/mpeg', 'audio/ogg'):
            return
    raise BadRequestError('Bad file type')

def unique_filename(orig_filename):
    new = simpleflake.simpleflake()
    filename = re.sub(r'^.+(\.[a-zA-Z0-9]+)$', r'%s\1' % new, orig_filename)
    # TODO:  file extension should be assigned based on mime type, or detected
    # file format.  Mime type should also be stored in the db record.
    if filename == orig_filename:
        raise BadRequestError('Bad file name')
    return filename

@app.route('/sound/<int:id>.json')
def view_sound(id):
    """
    API:  View one sound record
    """
    s = sound.Sound.get(sound.Sound.id == id)
    return jsonify(s.for_api(app.config['STORAGE']))

@app.route('/sound/<int:id>.json', methods=['DELETE'])
def delete_sound(id):
    """
    API:  Delete a sound record

    Querystring parameter:  auth_token
    """
    try:
        s = sound.get_with_auth_token(id,
                                      request.args.get('auth_token'),
                                      app.config)
        container = 'container_1'
        base_path = app.config['STORAGE'][container]['fs_path']
        if not base_path.endswith('/'):
            base_path += '/'
        unlink(base_path + s.basename)
        s.delete_instance()
        return jsonify({'status': 'OK'})
    except sound.Sound.DoesNotExist:
        response = jsonify(message='Forbidden')
        response.status_code = 403
        return response
    except BadRequestError:
        response = jsonify(message='Bad Request')
        response.status_code = 400
        return response

@app.route('/sound/<int:id>.json', methods=['PUT'])
def edit_sound(id):
    """
    API:  Edit a sound record

    Querystring parameters: auth_token(required)
    Request body parameters:  lat, lng, title
    """
    try:
        s = sound.get_with_auth_token(id,
                                      request.args.get('auth_token'),
                                      app.config)
        data = form_or_json()
        flags = 0
        if 'lat' in data:
            s.lat = float(data['lat'])
        if 'lng' in data:
            s.lng = float(data['lng'])
        if 'title' in data:
            s.title = data['title'].strip()
        if 'looping' in data and data['looping']:
            s.flags |= sound.LOOPING
        s.save()
        return jsonify(s.for_api(app.config['STORAGE']))
    except sound.Sound.DoesNotExist:
        response = jsonify(message='Forbidden')
        response.status_code = 403
        return response
    except ValueError:
        response = jsonify(message='Bad Request')
        response.status_code = 400
        return response

@app.route('/sounds/near/<float:lat>,<float:lng>,<int:meters>.json')
def sounds_near(lat, lng, meters):
    """
    Retrieve sounds near coordinates, within given distance in meters.
    """
    return jsonify({'sounds': sound.sounds_near(lat, lng,
                                                meters,
                                                app.config['STORAGE'])})

@app.route('/sounds/mine.json')
def sounds_for_user():
    try:
        sounds = sound.get_all_for_auth_token(request.args.get('auth_token'),
                                              app.config)
        return jsonify({'sounds': sounds})
    except sound.Sound.DoesNotExist:
        return jsonify({'sounds': []})
    except BadRequestError:
        response = jsonify(message='Bad Request')
        response.status_code = 400
        return response

