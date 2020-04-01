import cv2


def resize(frame, width: int):
    orig_h, orig_w, _ = frame.shape
    scale = orig_w / width
    height = round(orig_h / scale)
    return cv2.resize(frame, (width, height))
