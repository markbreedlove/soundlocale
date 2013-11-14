# Copyright (C) 2013  Mark Breedlove
# See README.md and License.txt.

"""
User-related view functions
"""

__all__ = ['add_user', 'get_user', 'activation']


from flask import jsonify, url_for, render_template, redirect, session
from ourcrypto import sign, unsign
from itsdangerous import BadSignature
from flask_mail import Mail, Message
from simpleflake import simpleflake
from peewee import DoesNotExist
import models.user as user
from ourexceptions import *
from util import form_or_json
from app import app


@app.route('/users.json', methods=['POST'])
def add_user():
    data = form_or_json()
    try:
        new_user = user.add_user(username=data['username'],
                                 fullname=data['fullname'],
                                 password=data['password'],
                                 email=data['email'])
        send_activation_mail(new_user.id, new_user.email)
        return jsonify({'id': new_user.id, 'username': new_user.username,
                        'fullname': new_user.fullname, 'email': new_user.email})
    except BadRequestError:
        response = jsonify(message='Bad Request')
        response.status_code = 400
        return response
    except ConflictError as e:
        response = jsonify(message=e.message)
        response.status_code = 409
        return response

@app.route('/user/<int:id>.json')
def get_user(id):
    try:
        the_user = user.User.get(user.User.id == id)
        return jsonify({'id': str(the_user.id), 'username': the_user.username,
                        'fullname': the_user.fullname, 'email': the_user.email})
    except DoesNotExist:
        response = jsonify(message='Not Found')
        response.status_code = 404
        return response

@app.route('/activation/<signedstring>')
def activation(signedstring):
    try:
        id = int(unsign(signedstring, app.config))
        the_user = user.User.get(user.User.id == id)
        the_user.status = 1
        the_user.auth_token = str(simpleflake())
        the_user.save()
        session['user_id'] = id
        return redirect(url_for('index'))
    except (BadSignature, DoesNotExist):
        response = jsonify(message='Bad Request')
        response.status_code = 400
        return response

def send_activation_mail(user_id, email):
    url = url_for('activation', signedstring=sign(str(user_id), app.config),
                  _external=True)
    mail = Mail(app)
    msg = Message('Activate your account', recipients=[email],
                  sender='mb@markbreedlove.com')
    msg.body = render_template('email.activation.txt', url=url)
    msg.html = render_template('email.activation.html', url=url)
    mail.send(msg)


