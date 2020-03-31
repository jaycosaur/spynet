## Before you start

### Setting Up Devices

Edge based devices will need to have Docker and Docker Compose installed (additionally optionally git). I have not included instructions on how to set this up as it is widely available at other sources.

Install Docker + Compose: https://dev.to/rohansawant/installing-docker-and-docker-compose-on-the-raspberry-pi-in-5-simple-steps-3mgl
Install Docker Compose: https://docs.docker.com/compose/install/

## Whats Included

Included in this guide are two types of devices:

1. **Hub** - A centralised service that is responsible for hosting the messaging networks, receiving messages from edge nodes and either processing itselfs or forwarding events for processing by another service.

2. **Node** - An edge device that will harbour a camera device and stream back captured images to a Hub on the local network.

3. **Edge-Hub** - _PLANNED_ A lightweight Hub that can be used to build fault tolerant mesh networks and acts as a message broker back to the main network Hub.

## Frequently Asked Questions

#### Can I have multiple hubs on the same network?

In general, yes. However nodes will stream to whichever hub they find first on the network with the same network id. If you which to run multiple hubs and specific nodes for those hubs, such as in a zoned or task based vision network, then you can just use a separate network id for separate zones.
