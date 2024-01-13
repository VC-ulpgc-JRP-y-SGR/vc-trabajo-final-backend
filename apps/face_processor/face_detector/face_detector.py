
import numpy as np
from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import List

@dataclass
class Point:
    x : float
    y : float

@dataclass
class BoundingBox:
    origin : Point
    end: Point

@dataclass
class FaceDetectorResult:
    image : np.ndarray 
    bounding_box : BoundingBox

class FaceDetector(ABC):
    @abstractmethod
    def detect(self, image : np.ndarray) -> List[FaceDetectorResult]:
        pass