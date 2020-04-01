import logging
import sys
import os
import typing
import threading

from flask import Flask, Response, jsonify
from flask_cors import CORS
import cv2

from streaming_helpers import CameraInformation


logging.getLogger("werkzeug").disabled = True
os.environ["WERKZEUG_RUN_MAIN"] = "true"


CLI = sys.modules["flask.cli"]
CLI.show_server_banner = lambda *x: None  # type: ignore

APP = Flask(__name__,)
CORS(APP)

node_services: typing.Dict[str, CameraInformation] = {}


def from_queue(camera_id: str):
    service = node_services.get(camera_id)
    while service:
        image = service.read_frame()
        res, im_jpg = cv2.imencode(".jpg", image)  # type: ignore
        if res:
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + im_jpg.tostring() + b"\r\n"
            )
    return None


@APP.route("/nodes", methods=["GET"])
def active_cameras():
    cameras = [dict(nodeId=service.node_id, isOnline=service.is_online) for service in node_services.values()]
    return jsonify(cameras)


@APP.route("/nodes/<node_id>/video_feed", methods=["GET"])
def video_feed(node_id: str):
    return Response(
        from_queue(node_id), mimetype="multipart/x-mixed-replace; boundary=frame"
    )


class StreamingService:
    def __init__(self, host="localhost", port=5000):
        self.host = host
        self.port = port
        self._thread = None

    def _run(self):
        print("starting streaming server on %s:%d" % (self.host, self.port))
        print("visit %s:%d to view live camera stream" % (self.host, self.port))
        APP.run(host=self.host, port=self.port, debug=False, use_reloader=False)

    def start(self):
        thread = threading.Thread(target=self._run, daemon=True)
        thread.start()
        self._thread = thread

    def hub_message_handler(self, cam_id, image):
        node_service = node_services.get(cam_id)
        if not node_service:
            node_service = CameraInformation(cam_id)
            node_services[cam_id] = node_service
        node_service.write_frame(image)
