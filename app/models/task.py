from datetime import datetime as dt

from peewee import CharField, BooleanField, DateTimeField, ForeignKeyField

from db import db
from models.user import User


class Task(db.Model):  # key for this model is TITLE

    title = CharField(unique=True)
    text = CharField()
    is_important = BooleanField()
    created_at = DateTimeField(default=dt.now)
    user = ForeignKeyField(User, backref="user")
