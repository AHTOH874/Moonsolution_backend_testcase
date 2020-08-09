from datetime import datetime as dt

from peewee import Model, CharField, DateTimeField, BooleanField, ForeignKeyField
from models.user import User


def migrate(migrator, database, fake=False, **kwargs):

    @migrator.create_model
    class Task(Model):
        title = CharField(unique=True)
        text = CharField()
        is_important = BooleanField()
        created_at = DateTimeField(default=dt.now)
        user = ForeignKeyField(User, backref="user")


def rollback(migrator, database, fake=False, **kwargs):
    migrator.remove_model('task')
