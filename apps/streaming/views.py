from flask import Blueprint, Flask, Response, request
from .model import NetworkCamera
from db import Camera, db

blueprint = Blueprint('streaming', __name__, url_prefix='/streaming')

@blueprint.route('/front_camera/')
def front_video_camera():
    camera = Camera.select().where(Camera.cam_type == 'front').first()
    camera = NetworkCamera(camera.ip, camera.port, 4096)
    return Response(camera.generator(), mimetype='multipart/x-mixed-replace; boundary=frame')

@blueprint.route('/side_camera/')
def side_video_camera():
    camera = Camera.select().where(Camera.cam_type == 'side').first()
    camera = NetworkCamera(camera.ip, camera.port, 4096)
    return Response(camera.generator(), mimetype='multipart/x-mixed-replace; boundary=frame')

@blueprint.route('/client_entered/')
def detected_client_entered():
    return {
        "status" : "ok"
    }

@blueprint.route('/client_exited/')
def detected_client_exited():
    return {
        "status" : "ok"
    }