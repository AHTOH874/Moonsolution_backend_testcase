from datetime import datetime as dt
from hashlib import sha256

from peewee import CharField, DateTimeField

from db import db
from config import config


class User(db.Model):

    login = CharField(unique=True)
    password = CharField()
    created_at = DateTimeField(default=dt.now)

    def set_password(self, password):
        self.password = sha256((password+config['secure']['salt_password']).encode()).hexdigest()

    def check_password(self, value):
        return (
            self.password == sha256((value+config['secure']['salt_password']).encode()).hexdigest()
        )
