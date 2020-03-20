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
