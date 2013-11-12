# Copyright (C) 2013  Mark Breedlove
# See README.md and License.txt.

"""
Authentication-related view functions
"""

__all__ = ['auth_token', 'add_session', 'delete_session']


from flask import jsonify, session, request, Response
from exceptions import KeyError
from peewee import DoesNotExist
from ourcrypto import sign, unsign
import hashlib
from app import app
import models.user as user
from ourexceptions import *
from util import form_or_json
from simpleflake import simpleflake


@app.route('/auth_token.json')
def auth_token():
    """
    Get the logged-in account's auth token, based on the session.  A session
    cookie must be present.  There are no parameters.
    """
    if 'user_id' in session:
        the_user = user.User.get(user.User.id == int(session['user_id']))
        if the_user.auth_token:
            response = jsonify(auth_token=sign(the_user.auth_token, app.config),
                               user_id=str(session['user_id']))
        else:
            response = jsonify(message='Not Found')
            response.status_code = 404
        return response
    else:
        response = jsonify(message='Unauthorized')
        response.status_code = 401
        return response


@app.route('/session.json', methods=['POST'])
def add_session():
    """
    Create a "session" by taking the email and password, and returning
    an auth token and setting the user ID in the session cookie.
    """
    data = form_or_json()
    try:
        the_user = user.User.get(user.User.email == data['email'])
        if the_user.password == hashlib.sha256(data['password']).hexdigest():
            session['user_id'] = the_user.id
            if the_user.auth_token:
                auth_token = the_user.auth_token
            else:
                auth_token = str(simpleflake())
                the_user.auth_token = auth_token
                the_user.save()
            return jsonify(auth_token=sign(auth_token, app.config),
                           user_id=str(the_user.id))
        else:
            raise Exception()
    except KeyError:
        response = jsonify(message='Bad Request')
        response.status_code = 400
        return response
    except DoesNotExist:
        response = jsonify(message='Unauthorized')
        response.status_code = 401
        return response

@app.route('/session.json', methods=['DELETE'])
def delete_session():
    if 'user_id' in session:
        del(session['user_id'])
    return jsonify(status='OK')

