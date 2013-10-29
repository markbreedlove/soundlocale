
__all__ = ['add_sound', 'view_sound', 'delete_sound', 'edit_sound',
           'sounds_near']

from flask import jsonify, request
import models.sound as sound
import models.user as user
from util import form_or_json
from app import app, cfg
from werkzeug import secure_filename


@app.route('/user/<int:user_id>/sounds.json', methods=['POST'])
def add_sound(user_id):
    """
    Add a sound file

    Querystring parameters:  lat, lng, title
    POST data (application/json or application/x-www-form-urlencoded):
      soundfile

    Returns ID of newly-created sound resource, as: {"id": <the id>}
    """
    the_user = user.User.get(user.User.id == user_id)
    lat = float(request.args.get('lat'))
    lng = float(request.args.get('lng'))
    title = request.args.get('title')
    container = 'container_1'
    file = request.files['soundfile']
    file_name = secure_filename(file.filename)
    file.save(cfg['storage'][container]['fs_path'] + file_name)
    new_sound = sound.add_sound(lat=lat, lng=lng, title=title,
                                basename=file_name, container=container,
                                user=the_user)
    return jsonify({'id': new_sound.id})

@app.route('/sound/<int:id>.json')
def view_sound(id):
    """
    API:  View one sound record
    """
    s = sound.Sound.get(sound.Sound.id == id)
    return jsonify(s.for_api(cfg['storage']))

@app.route('/sound/<int:id>.json', methods=['DELETE'])
def delete_sound(id):
    """
    API:  Delete a sound record
    """
    s = sound.Sound.get(sound.Sound.id == id)
    container = 'container_1'
    base_path = cfg['storage'][container]['fs_path']
    if not base_path.endswith('/'):
        base_path += '/'
    os.unlink(base_path + s.basename)
    s.delete_instance()
    return jsonify({'status': 'OK'})

@app.route('/sound/<int:id>.json', methods=['PUT'])
def edit_sound(id):
    """
    API:  Edit a sound record
    """
    s = sound.Sound.get(sound.Sound.id == id)
    if 'lat' in request.form:
        s.lat = float(request.form['lat'])
    if 'lng' in request.form:
        s.lng = float(request.form['lng'])
    if 'title' in request.form:
        s.title = request.form['title']
    s.save()
    return jsonify(s.for_api(cfg['storage']))

@app.route('/sounds/near/<float:lat>,<float:lng>,<int:meters>.json')
def sounds_near(lat, lng, meters):
    """
    Retrieve sounds near coordinates, within given distance in meters.
    """
    return jsonify({'sounds': sound.sounds_near(lat, lng,
                                                meters, cfg['storage'])})


