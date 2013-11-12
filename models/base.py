# Copyright (C) 2013  Mark Breedlove
# See README.md and License.txt.

import peewee
from models import db

class BaseModel(peewee.Model):
    class Meta:
        database = db

