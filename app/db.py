import peewee

from config import config

db = peewee.PostgresqlDatabase(
    config['db'].pop('db'),
    **config['db'],
    autorollback=True
)


class BaseModel(peewee.Model):
    class Meta:
        database = db


db.Model = BaseModel
