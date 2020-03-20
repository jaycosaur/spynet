from vision_network import node, camera

cv_camera = camera.CvCamera(400)
node = node.Node(node_id="special_cam", camera=cv_camera, network_id="special")

try:
    node.start()
    input("Waiting...")
finally:
    cv_camera.release()
    node.stop()
