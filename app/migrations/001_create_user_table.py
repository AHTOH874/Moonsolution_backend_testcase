from datetime import datetime as dt

from peewee import Model, CharField, DateTimeField


def migrate(migrator, database, fake=False, **kwargs):

    @migrator.create_model
    class User(Model):
        login = CharField(unique=True)
        password = CharField()
        created_at = DateTimeField(default=dt.now)

def rollback(migrator, database, fake=False, **kwargs):
    migrator.remove_model('user')
