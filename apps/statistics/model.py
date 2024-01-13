from peewee import *
from db import db

class Entrances(Model):
    timestamp = DateTimeField()
    genre = CharField()
    age_interval = CharField()
    image = BlobField()

    def to_json(self):
        return {
            'timestamp': self.timestamp,
            'genre': self.genre,
            'age_interval': self.age_interval,
        }

    class Meta:
        database = db # This model uses the "people.db" database.

class Counter(Model):
    value = IntegerField()
    timestamp = DateTimeField()

    class Meta:
        database = db