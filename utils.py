import numpy as np
import cv2

from apps.face_processor.face_detector.face_detector import BoundingBox


class ImageUtils:
    @staticmethod
    def crop(image : np.array, bounding_box : BoundingBox) -> np.ndarray:
        return image[bounding_box.origin.x:bounding_box.end.x, bounding_box.origin.y:bounding_box.end.y]
    
    @staticmethod
    def overlay_icon(image: np.array, icon_path: str, color: tuple, icon_size : int, point : tuple) -> np.ndarray:
        icon = cv2.imread(icon_path, cv2.IMREAD_GRAYSCALE)
        icon = cv2.resize(icon, (icon_size, icon_size))
        mask = icon == 0
        color_layer = np.full((icon.shape[0], icon.shape[1], 3), color, dtype=np.uint8)
        np.copyto(image[point[1]-icon.shape[0]//2:point[1]+icon.shape[0]//2, point[0]-icon.shape[1]//2:point[0]+icon.shape[1]//2], color_layer, where=mask[:,:,None])
        return image