from apps.cameras.model import Camera
import argparse

def change_camera(ip, port, cam_type):
    try:
        camera = Camera.select().where(Camera.cam_type == cam_type).get()
        camera.ip = ip
        camera.port = port
        camera.save()
        return {"status": "ok"}
    except:
        new_camera = Camera(cam_type=cam_type, ip=ip, port=port)
        new_camera.save()
        return {"status" : "ok"}


parser = argparse.ArgumentParser("ip")
parser.add_argument("--ip", type=str, help="The ip to listen on")
parser.add_argument("--cam_type", type=str, help="The cam_type to listen on")
parser.add_argument("--port", type=str, help="The port to listen on")
args = parser.parse_args()
change_camera(args.ip, args.port, args.cam_type)
