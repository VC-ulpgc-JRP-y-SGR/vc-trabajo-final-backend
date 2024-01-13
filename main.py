from flask import Flask
from apps.statistics.model import Entrances
from db import Camera, db
from apps.cameras.views import blueprint as cameras_blueprint
from apps.streaming.views import blueprint as streaming_blueprint
from apps.statistics.views import blueprint as statistics_blueprint
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy   dog'
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app, resources={r"/*": {"origins": "*"}})
db.connect()
db.create_tables([Camera, Entrances])
app.register_blueprint(blueprint=cameras_blueprint)
app.register_blueprint(blueprint=streaming_blueprint)
app.register_blueprint(blueprint=statistics_blueprint)

def start():
    app.run(debug=True)

start()