
__all__ = ['add_user', 'get_user']


from flask import jsonify
import models.user as user
from util import form_or_json
from app import app


@app.route('/users.json', methods=['POST'])
def add_user():
    data = form_or_json()
    new_user = user.add_user(username=data['username'],
                             fullname=data['fullname'],
                             password=data['password'],
                             email=data['email'])
    return jsonify({'id': new_user.id, 'username': new_user.username,
                    'fullname': new_user.fullname, 'email': new_user.email})

@app.route('/user/<int:id>.json')
def get_user(id):
    the_user = user.User.get(user.User.id == id)
    # TODO: return 404 if empty?
    return jsonify({'id': the_user.id, 'username': the_user.username,
                    'fullname': the_user.fullname, 'email': the_user.email})

