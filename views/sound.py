# Copyright (C) Mark Breedlove and Qingyang Xi
# See README.md and License.txt.

"""
Sound file-related view functions
"""

__all__ = ['add_sound', 'view_sound', 'delete_sound', 'edit_sound',
           'sounds_near']

from flask import jsonify, request
from os import unlink
import simpleflake
import re
import subprocess
from distutils import spawn
import models.sound as sound
import models.user as user
# from util import form_or_json, async
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
        soundfile = request.files['soundfile']
        ftype = filetype(soundfile.filename)
        (filename, base) = unique_filename(soundfile.filename)
        fullpath = app.config['STORAGE'][container]['fs_path'] + filename
        soundfile.save(fullpath)

        flags |= transcode(fullpath, ftype)

        new_sound = sound.add_sound(lat=lat, lng=lng, title=title,
                                    basename=str(base), container=container,
                                    user=u, flags=flags)
        return jsonify(new_sound.for_api(app.config['STORAGE']))
    except user.User.DoesNotExist:
        raise UnauthorizedError()
    except ValueError as e:
        raise BadRequestError(e.message)

def filetype(filename):
    pat  = re.compile(r"\.(mp3|ogg|m4a|aif|wav)$", re.I)
    m = pat.search(filename)
    if (m):
        return m.groups(0)[0].lower()
    else:
        raise BadRequestError('Bad file type')

def unique_filename(orig_filename):
    base = simpleflake.simpleflake()
    filename = re.sub(r'^.+(\.[a-zA-Z0-9]+)$', r'%s\1' % base, orig_filename)
    # TODO:  file extension should be assigned based on mime type, or detected
    # file format.  Mime type should also be stored in the db record.
    if filename == orig_filename:
        raise BadRequestError('Bad file name')
    return (filename, base)

def transcode(filename, orig_file_type):
    """
    Hand off the transcoding of the audio file to the appropriate function for
    its filetype.  Return a bitmask indicating what types of derivatives are
    in storage.
    """
    try:
        _transcode(filename, orig_file_type)
        if orig_file_type == 'mp3':
            return sound.MP3 | sound.OGG
        else:
            return sound.M4A | sound.OGG
    except:
        app.logger.warn('avconv not process %s file %s' % (orig_file_type,
                                                           filename))
        raise BadRequestError('Could not process this file')

# @async
def _transcode(filename, orig_file_type):
    """
    Actually transcode the audio file, depending on its source format.
    It would be nice if this could run asynchronously, but error handling
    becomes much more involved that way.
    """
    if orig_file_type == 'mp3':
        transcode_to_ogg(filename)
    elif orig_file_type == 'm4a':
        transcode_to_ogg(filename)
    elif orig_file_type == 'ogg':
        transcode_to_m4a(filename)
    elif orig_file_type == 'aif':
        transcode_to_ogg(filename)
        transcode_to_m4a(filename)
        unlink(filename)
    elif orig_file_type == 'wav':
        transcode_to_ogg(filename)
        transcode_to_m4a(filename)
        unlink(filename)

def transcode_to_ogg(filename):
    dest_name = re.sub(r'^(.*)\.[a-z34]+$', r'\1.ogg', filename)
    _call_avconv(filename, dest_name, ['-acodec', 'libvorbis', '-q:a', '7'])

def transcode_to_m4a(filename):
    dest_name = re.sub(r'^(.*)\.[a-z34]+$', r'\1.m4a', filename)
    _call_avconv(filename, dest_name, ['-strict', 'experimental', '-vbr', '5'])

def _call_avconv(infile, outfile, extra_args=None):
    avconv = spawn.find_executable('avconv')
    extra_args = extra_args or []
    opts = [avconv, '-i', infile] + extra_args + [outfile]
    with open('/dev/null', 'w') as devnull:
        subprocess.check_call(opts, stderr=devnull)

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
        delete_files(s.basename, s.container, s.flags)
        s.delete_instance()
        return jsonify({'status': 'OK'})
    except sound.Sound.DoesNotExist:
        raise ForbiddenError()

def delete_files(basename, container, flags):
    base_path = app.config['STORAGE'][container]['fs_path']
    if not base_path.endswith('/'):
        base_path += '/'
    if flags & sound.MP3:
        unlink(base_path + basename + '.mp3')
    if flags & sound.M4A:
        unlink(base_path + basename + '.m4a')
    if flags & sound.OGG:
        unlink(base_path + basename + '.ogg')
    
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
        raise ForbiddenError()
    except ValueError:
        raise BadRequestError()

@app.route('/sounds/near/<float:lat>,<float:lng>,<int:meters>.json')
def sounds_near(lat, lng, meters):
    """
    Retrieve sounds near coordinates, within given distance in meters.
    """
    user_id = request.args.get('user_id')
    return jsonify({'sounds': sound.sounds_near(lat, lng, meters,
                                                app.config['STORAGE'],
                                                user_id)})

@app.route('/sounds/mine.json')
def sounds_for_user():
    try:
        sounds = sound.get_all_for_auth_token(request.args.get('auth_token'),
                                              app.config)
        return jsonify({'sounds': sounds})
    except sound.Sound.DoesNotExist:
        return jsonify({'sounds': []})

