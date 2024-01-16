import datetime
import threading
import argparse
import cv2
from flask import Flask, send_file
from apps.face_processor.face_detector.mediapipe import MediaPipeFaceDetector
from apps.face_processor.face_qualifier import FaceQualifier
from apps.statistics.model import Counter, Entrances
from apps.streaming.model import NetworkCamera
from db import Camera, db
from apps.cameras.views import blueprint as cameras_blueprint
from apps.streaming.views import blueprint as streaming_blueprint
from apps.statistics.views import blueprint as statistics_blueprint, entrances
import sys
from flask_cors import CORS
from flask_socketio import SocketIO, emit

from predictor import make_prediction

app = Flask(__name__)
db.connect()
db.create_tables([Camera, Entrances, Counter])
app.register_blueprint(blueprint=cameras_blueprint)
app.register_blueprint(blueprint=streaming_blueprint)
app.register_blueprint(blueprint=statistics_blueprint)

CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading", logger=True, engineio_logger=True)


def client_has_entered():
    try:
        results = make_prediction()
        image = results['image']
        generate_hash = str(hash(datetime.datetime.now()))
        image.save("./statics/" + generate_hash + '.jpg')
        entrance = Entrances.create(timestamp=datetime.datetime.now(),
                                    genre=results['genre'],
                                    age_interval=results['age'],
                                    image=generate_hash + '.jpg')
    except:
        pass
    Counter(value=1, timestamp=datetime.datetime.now()).save()
    socketio.emit('visitors', {'visitors': 'Lets dance'}, namespace='/visitors')


@app.route('/images/<image_name>/')
def get_image(image_name):
    return send_file('./statics/' + image_name, mimetype='image/jpg')

@app.route('/client_entered/', methods=['POST'])
def detected_client_entered():
    thread = threading.Thread(target=client_has_entered)
    thread.start()
    return {"status": "ok"}

@app.route('/client_exited/', methods=['POST'])
def detected_client_exited():
    Counter(value=-1, timestamp=datetime.datetime.now()).save()
    socketio.emit('visitors', {'visitors': 'Lets dance'}, namespace='/visitors')
    return {"status": "ok"}

@socketio.on('connect', namespace='/visitors')
def test_connect():
    pass

#pass ip by args 

def start():
    parser = argparse.ArgumentParser("ip")
    parser.add_argument("--ip", type=str, default="127.0.0.1", help="The ip to listen on")
    args = parser.parse_args()
    socketio.run(app, debug=True, host=args.ip, port=5000)

if __name__ == "__main__":
    start()