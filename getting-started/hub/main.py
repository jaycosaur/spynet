import os
from vision_network.hub import Hub

NETWORK_ID = os.getenv("NETWORK_ID")
if not NETWORK_ID:
    raise Exception("NETWORK_ID env variable is not set!")


def message_handler(cam_id, image):
    print(f"Received image from {cam_id} of shape {image.shape}")


hub = Hub(network_id=NETWORK_ID, message_handler=message_handler)

try:
    hub.start()
    input("waiting ...")
finally:
    print("Stopping...")
    hub.stop()
