from .face_detector import BoundingBox, FaceDetector, FaceDetectorResult, Point
from typing import List
import cv2
import numpy as np
import os
import mediapipe as mp
import numpy as np
from dataclasses import dataclass
from typing import Any, List
import numpy as np

from utils import ImageUtils

class MediaPipeFaceDetector(FaceDetector):
    def detect(self, image : np.ndarray) -> List[FaceDetectorResult]:
        BaseOptions = mp.tasks.BaseOptions
        FaceDetector = mp.tasks.vision.FaceDetector
        FaceDetectorOptions = mp.tasks.vision.FaceDetectorOptions
        VisionRunningMode = mp.tasks.vision.RunningMode

        options = FaceDetectorOptions(
            base_options=BaseOptions(model_asset_path='./models/blaze_face_short_range.tflite'),
            running_mode=VisionRunningMode.IMAGE)

        with FaceDetector.create_from_options(options) as detector:
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)
            face_detector_result = detector.detect(mp_image)
            return self._convert_to_face_detector_result(image, [(x.bounding_box.origin_x, x.bounding_box.origin_y, x.bounding_box.width, x.bounding_box.height) for x in face_detector_result.detections])
        
    def _convert_to_face_detector_result(self, image, faces) -> List[FaceDetectorResult]:
        bounding_boxes = [BoundingBox(Point(x, y), Point(x + w, y + h)) for (x, y, w, h) in faces]
        return [FaceDetectorResult(ImageUtils.crop(image, bounding_box), bounding_box) for bounding_box in bounding_boxes]
    