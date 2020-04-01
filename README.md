# SpyNet - Distributed Vision Networking

## WORK IN PROGRESS

Includes:

1. Auto-discovery of camera nodes via zeroconf networking.
2. ZeroMQ messaging from nodes to hub, courtesy of ImageZMQ.
3. Integrated camera producers: OpenCV
4. 3 line setup for camera node, 3 line setup for hub

Much of the time invested into setting up distrubted vision networks is in device setup, dependency compilation, device management and software deployment.

The philosophy of this project is to be able to build locally, cross-compile and deploy on edge-based devices running containerised services (Dockerfiles) with a light manager (Docker Compose). Both of which are well supported on a wide range of devices. This allows fast setup of devices (as dependencies will be within the docker containers), and allow the developer to build and deploy services fast, to focus their efforts on the valuable hub processing / data analytics.

## Getting Started (Edge Devices)

For how to get started on edge-devices please see the instructions in the [getting started guide](https://github.com/jaycosaur/distributed-vision-networking/tree/master/getting-started).

Currently the system has been tested as working and functional on several ARM based devices:

1. Raspberry Pi 3b
2. Raspberry Pi 3b+
3. Raspberry Pi 4b
4. Raspberry Pi Zero (INCOMPLETE TESTING)
5. Raspberry Pi Zero Wireless
6. Jetson Nano (INCOMPLETE TESTING)

## Getting Started Laptop / Desktop

## HUB

```python
from vision_network import hub
import cv2


def message_handler(cam_id, image):
    print(f"Received image from {cam_id} of shape {image.shape}")


hub = hub.Hub(network_id="special", message_handler=message_handler)

try:
    hub.start()
    input("waiting ...")
finally:
    print("Stopping...")
    hub.stop()
```

## NODE

```python
from vision_network import node, camera

cv_camera = camera.CvCamera(400)
node = node.Node(node_id="special_cam", camera=cv_camera, network_id="special")

try:
    node.start()
    input("Waiting...")
finally:
    cv_camera.release()
    node.stop()
```

Usage on mac:

Hub processes incoming messages in thread, to view images on mac you will need to pass these through a queue to the main thread for rendering due to imshow restriction on darwin.
