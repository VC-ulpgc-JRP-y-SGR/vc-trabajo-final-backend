import datetime
from flask import Flask
from apps.statistics.model import Counter, Entrances
from db import Camera, db
from apps.cameras.views import blueprint as cameras_blueprint
from apps.streaming.views import blueprint as streaming_blueprint
from apps.statistics.views import blueprint as statistics_blueprint
from flask_cors import CORS
from flask_socketio import SocketIO, emit

app = Flask(__name__)
db.connect()
db.create_tables([Camera, Entrances, Counter])
app.register_blueprint(blueprint=cameras_blueprint)
app.register_blueprint(blueprint=streaming_blueprint)
app.register_blueprint(blueprint=statistics_blueprint)

CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading", logger=True, engineio_logger=True)

@app.route('/client_entered/', methods=['POST'])
def detected_client_entered():
    Counter(value=1, timestamp=datetime.datetime.now()).save()
    socketio.emit('visitors', {'visitors': 'Lets dance'}, namespace='/visitors')
    return {"status": "ok"}

@app.route('/client_exited/', methods=['POST'])
def detected_client_exited():
    Counter(value=-1, timestamp=datetime.datetime.now()).save()
    socketio.emit('visitors', {'visitors': 'Lets dance'}, namespace='/visitors')
    return {"status": "ok"}

@socketio.on('connect', namespace='/visitors')
def test_connect():
    pass

def start():
    socketio.run(app, debug=True)

if __name__ == "__main__":
    start()