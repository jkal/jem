import peewee
from jem.models import db_proxy

def get_or_create(cls, **kwargs):
    try:
        with db_proxy.transaction():
            return cls.create(**kwargs).execute()
    except peewee.IntegrityError:
        return cls.select().filter(**kwargs).execute()
