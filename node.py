from vision_network.node import Node
from vision_network.camera import CvCamera

cv_camera = CvCamera(400)
node = Node(node_id="special_cam", camera=cv_camera, network_id="special")
node.start()

try:
    input("Waiting...")
finally:
    cv_camera.release()
    node.stop()
