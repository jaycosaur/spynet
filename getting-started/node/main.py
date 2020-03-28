import os
from vision_network import node, camera

NODE_ID = os.getenv("NODE_ID")
NETWORK_ID = os.getenv("NETWORK_ID")

if not NODE_ID:
    raise Exception("NODE_ID env variable is not set!")
if not NETWORK_ID:
    raise Exception("NETWORK_ID env variable is not set!")

cv_camera = camera.CvCamera(400)

node_service = node.Node(node_id=NODE_ID, network_id=NETWORK_ID, camera=cv_camera,)

try:
    node_service.start()
    input("Waiting...")
finally:
    cv_camera.release()
    node_service.stop()
