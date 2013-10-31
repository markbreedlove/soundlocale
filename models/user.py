'''

Usage examples:

    from models import db
    import models.user as user
    db.init('dbname', user='user', passwd='password', host='host')
    the_user = user.User.get(user.User.username == 'name')
    print the_user.email
    new_user = user.add_user('name', 'Full Name', 'password', 'usr@domain.tld')
'''

import peewee
from _mysql_exceptions import IntegrityError
import hashlib
import re
import simpleflake
from base import BaseModel
from ourexceptions import *

class User(BaseModel):
    id = peewee.BigIntegerField(primary_key=True)
    username = peewee.CharField()
    fullname = peewee.CharField()
    password = peewee.CharField()
    email = peewee.CharField()
    status = peewee.IntegerField()

def add_user(username, fullname, password, email):
    if not re.match(r'^[a-z\d\-]+$', username, flags=re.I):
        raise BadRequestError('Bad username')
    if not re.match(r'^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,4}$',
                    email,
                    flags=re.I):
        raise BadRequestError('Bad email address')
    if not len(password) > 7:
        raise BadRequestError('Password is too short')
    if not re.match(r'[a-z]', fullname, re.I):
        raise BadRequestError('Full name appears not to be complete')
    try:
        return User.create(id=simpleflake.simpleflake(),
                           username=username.strip(),
                           fullname=fullname.strip(),
                           password=hashlib.sha256(password).hexdigest(),
                           email=email,
                           status=0)
    except IntegrityError:
        raise ConflictError('Account already exists')

