from flask import Blueprint, request
from .model import Camera
from pystreamapi import Stream

blueprint = Blueprint('cameras', __name__, url_prefix='/cameras')

@blueprint.route('/', methods=['GET'])
def lists_camera():
    return Stream.of(list(Camera.select()))\
        .map(lambda c: c.to_json()).\
        to_list()
    
@blueprint.route('/', methods=['POST'])
def create_camera():
    camera_type = request.json['type']
    camera = Camera.select().where(Camera.cam_type == camera_type).first()

    if camera is None:
        camera = Camera.create(ip=request.json['ip'], port=request.json['port'], cam_type=request.json['type'])
        return camera.to_json()

    camera.ip = request.json['ip']
    camera.port = request.json['port']
    camera.save()
    return camera.to_json()
    