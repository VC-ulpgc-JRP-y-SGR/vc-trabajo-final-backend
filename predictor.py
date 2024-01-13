import cv2
import numpy as np
import PIL.Image as Pillow
from apps.face_processor.face_detector.mediapipe import MediaPipeFaceDetector
from apps.face_processor.face_qualifier import FaceQualifier
from apps.streaming.model import NetworkCamera
from db import Camera, db
from flask_cors import CORS

def make_prediction():
    camera = Camera.select().where(Camera.cam_type == 'front').first()
    camera = NetworkCamera(camera.ip, camera.port, 4096)
    frame = camera._receive_frame()
    detector = MediaPipeFaceDetector()
    detection = detector.detect(frame)
    frame = cv2.rectangle(frame, (detection[0].bounding_box.origin.x, detection[0].bounding_box.origin.y), (detection[0].bounding_box.end.x, detection[0].bounding_box.end.y), (0, 255, 0), 2)
    cropped_image = Pillow.fromarray(frame).crop((detection[0].bounding_box.origin.x, detection[0].bounding_box.origin.y, detection[0].bounding_box.end.x, detection[0].bounding_box.end.y))
    qualifier = FaceQualifier()
    results = qualifier.detect(np.array(cropped_image))
    return {
        "genre" : results[0],
        "age": results[1]
    }