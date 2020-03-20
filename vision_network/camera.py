import typing
from abc import ABC, abstractmethod

import cv2

from .utils import image as image_utils


class CameraBase(ABC):
    @abstractmethod
    def read(self) -> typing.Tuple[bool, typing.Any]:
        ...

    @abstractmethod
    def release(self) -> None:
        ...


class CvCamera(CameraBase):
    def __init__(self, width: int, cam_id=0):
        self.__camera = cv2.VideoCapture(cam_id)
        self.__width = width

    def read(self):
        ok, frame = self.__camera.read()
        if not ok:
            return ok, None

        return ok, image_utils.resize(frame, self.__width)

    def release(self):
        self.__camera.release()
