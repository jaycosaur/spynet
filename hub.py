from spynet import hub
from streaming_service import StreamingService

streamer = StreamingService()

hub_service = hub.Hub(
    network_id="special", message_handler=streamer.hub_message_handler
)

streamer.start()

try:
    hub_service.start()
    input("press any key to stop...")
finally:
    print("Stopping...")
    hub_service.stop()
