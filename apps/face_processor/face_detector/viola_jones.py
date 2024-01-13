from .face_detector import BoundingBox, FaceDetector, FaceDetectorResult, Point
from typing import List
import cv2
import numpy as np
import os

from utils import ImageUtils

    
class ViolaJonesFaceDetector(FaceDetector):
    cascPathface = os.path.dirname(
        cv2.__file__) + "/data/haarcascade_frontalface_alt2.xml"

    def detect(self, image : np.ndarray) -> List[FaceDetectorResult]:
        faceCascade = cv2.CascadeClassifier(self.cascPathface)
        gray = self._convert_image_to_gray(image)
        faces = faceCascade.detectMultiScale(gray,
                                         scaleFactor=1.1,
                                         minNeighbors=5,
                                         minSize=(60, 60),
                                         flags=cv2.CASCADE_SCALE_IMAGE)
        return self._convert_to_face_detector_result(image, faces)
        
    
    def _convert_to_face_detector_result(self, image, faces) -> List[FaceDetectorResult]:
        bounding_boxes = [BoundingBox(Point(x, y), Point(x+w, y+h)) for (x, y, w, h) in faces]
        return [FaceDetectorResult(ImageUtils.crop(image, bounding_box), bounding_box) for bounding_box in bounding_boxes]
    
    def _convert_image_to_gray(self, image : np.ndarray) -> np.ndarray:
        import cv2
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)