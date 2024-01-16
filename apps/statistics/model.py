from peewee import *
from db import db

class Entrances(Model):
    timestamp = DateTimeField()
    genre = CharField()
    age_interval = CharField()
    image = CharField()

    def to_json(self):
        return {
            'id' : self.id,
            'timestamp': self.timestamp,
            'genre': self.genre,
            'age_interval': self.age_interval,
            'image': "/images/" + self.image +'/'
        }

    class Meta:
        database = db # This model uses the "people.db" database.

class Counter(Model):
    value = IntegerField()
    timestamp = DateTimeField()

    class Meta:
        database = db