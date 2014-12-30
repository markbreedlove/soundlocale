#!/usr/bin/env python

"""
Perform database migrations.

Example usage within Vagrant VM:
    $ SOUNDLOCALE_CONFIG=configuration_vagrant ./migrate.py
"""

import peewee
from psycopg2 import ProgrammingError
from app import app
from playhouse.migrate import *
from models import db
from models.user import User
from models.sound import Sound
from models.migration_log import MigrationLog

db.init(app.config['DB_NAME'],
        **{'password': app.config['DB_PASSWORD'],
           'host': app.config['DB_HOST'],
           'user': app.config['DB_USER']})
db.connect()

User.create_table(fail_silently=True)
Sound.create_table(fail_silently=True)

## TODO: migrations
# MigrationLog.create_table(fail_silently=True)
# max_id = MigrationLog.select(fn.Max(MigrationLog.id)).scalar()
# Generates error about PostgresqlMigrator not being defined:
# although see http://peewee.readthedocs.org/en/latest/peewee/playhouse.html#schema-migrations
# migrator = PostgresqlMigrator(db)
