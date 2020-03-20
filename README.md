# Distributed Vision Networking

## WORK IN PROGRESS

Includes:

1. Auto-discovery of camera nodes via zeroconf networking.
2. ZeroMQ messaging from nodes to hub.
3. Integrated camera producers: OpenCV
4. 3 line setup for camera node, 3 line setup for hub

Notes:

Hub processes incoming messages in thread, to view images on mac you will need to pass these through a queue to the main thread for rendering due to imshow restriction on darwin.
