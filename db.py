from peewee import *

db = SqliteDatabase('people.db')

class Camera(Model):
    ip = CharField()
    port = IntegerField()
    cam_type = CharField()

    def to_json(self):
        return {
            'id': self.id,
            'ip': self.ip,
            'port': self.port,
            'type': self.cam_type
        }

    class Meta:
        database = db # This model uses the "people.db" database.