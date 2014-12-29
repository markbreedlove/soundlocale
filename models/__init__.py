# Copyright (C) Mark Breedlove
# See README.md and License.txt.

import peewee
db = peewee.PostgresqlDatabase(None, threadlocals=True)
