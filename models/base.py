import peewee
from models import db

class BaseModel(peewee.Model):
    class Meta:
        database = db

