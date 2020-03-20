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
