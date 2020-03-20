# Distributed Vision Networking

## WORK IN PROGRESS

Includes:

1. Auto-discovery of camera nodes via zeroconf networking.
2. ZeroMQ messaging from nodes to hub.
3. Integrated camera producers: OpenCV
4. 3 line setup for camera node, 3 line setup for hub

Notes:

Hub processes incoming messages in thread, to view images on mac you will need to pass these through a queue to the main thread for rendering due to imshow restriction on darwin.

## HUB

```python
from vision_network.hub import Hub
import cv2


def message_handler(cam_id, image):
    print(f"Received image from {cam_id} of shape {image.shape}")


hub = Hub(network_id="special", message_handler=message_handler)
hub.start()

try:
    input("waiting ...")
finally:
    print("Stopping...")
    hub.stop()
```

## NODE

```python
from vision_network.node import Node
from vision_network.camera import CvCamera

cv_camera = CvCamera(400) # restrict image width to 400
node = Node(node_id="special_cam", camera=cv_camera, network_id="special")
node.start()

try:
    input("Waiting...")
finally:
    cv_camera.release()
    node.stop()
```
