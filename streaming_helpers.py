import queue
import time
import numpy as np


class CameraInformation:
    def __init__(self, cam_id: str):
        self._frame_queue: queue.Queue = queue.Queue(maxsize=1)
        self._frame_shape = None
        self._last_frame_time = None
        self.is_online = True
        self.node_id = cam_id

    def write_frame(self, frame):
        try:
            self._frame_queue.get_nowait()
        except queue.Empty:
            pass
        self._frame_shape = frame.shape
        self._last_frame_time = time.time()
        self._frame_queue.put_nowait(frame)

    def read_frame(self,):
        try:
            frame = self._frame_queue.get(timeout=2)
            if not self.is_online:
                self.is_online = True
            return frame
        except queue.Empty:
            if self.is_online:
                self.is_online = False
            return np.zeros(self._frame_shape)
