from utils import ImageUtils
from .face_detector import BoundingBox, FaceDetector, FaceDetectorResult, Point
import numpy as np
from typing import List
from retinaface import RetinaFace

class RetinafaceFaceDetector(FaceDetector):
    def detect(self, image : np.ndarray) -> List[FaceDetectorResult]:
        faces = RetinaFace.detect_faces(image);
        return self._convert_to_face_detector_result(image, [faces[key]['facial_area'] for key in faces.keys()])
    
    def _convert_to_face_detector_result(self, image, faces) -> List[FaceDetectorResult]:
        bounding_boxes = [BoundingBox(Point(x, y), Point(w, h)) for (x, y, w, h) in faces]
        return [FaceDetectorResult(ImageUtils.crop(image, bounding_box), bounding_box) for bounding_box in bounding_boxes]