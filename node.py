from spynet import node, camera

cv_camera = camera.CvCamera(400)
node_service = node.Node(
    node_id="special_cam_mac", camera=cv_camera, network_id="special"
)

try:
    node_service.start()
    input("Waiting...")
finally:
    cv_camera.release()
    node_service.stop()
