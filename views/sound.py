# Copyright (C) 2013  Mark Breedlove
# See README.md and License.txt.

"""
Sound file-related view functions
"""

__all__ = ['add_sound', 'view_sound', 'delete_sound', 'edit_sound',
           'sounds_near']

from flask import jsonify, request
from os import unlink
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
    POST data: lat, lng, title, flags, soundfile

    Returns ID of newly-created sound resource, as: {"id": <the id>}
    """
    try:
        u = user.get(auth_token=request.args.get('auth_token'),
                     config=app.config)
        data = form_or_json()
        lat = float(data['lat'])
        lng = float(data['lng'])
        title = data['title'].strip()
        flags = int(data['flags'])
        container = 'container_1'
        file = request.files['soundfile']
        file_name = secure_filename(file.filename)
        file.save(app.config['STORAGE'][container]['fs_path'] + file_name)
        new_sound = sound.add_sound(lat=lat, lng=lng, title=title,
                                    basename=file_name, container=container,
                                    user=u)
        return jsonify(new_sound.for_api(app.config['STORAGE']))
    except user.User.DoesNotExist:
        response = jsonify(message='Unauthorized')
        response.status_code = 401
        return response
    except (ValueError, BadRequestError):
        response = jsonify(message='Bad Request')
        response.status_code = 400
        return response

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
        if 'lat' in data:
            s.lat = float(data['lat'])
        if 'lng' in data:
            s.lng = float(data['lng'])
        if 'title' in data:
            s.title = data['title'].strip()
        if 'flags' in data:
            s.flags = int(data['flags'])
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

