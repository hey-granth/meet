from channels.generic.websocket import AsyncWebsocketConsumer
import json


class CallConsumer(AsyncWebsocketConsumer):
    """
    Consumer for handling WebSocket connections for call rooms.
    """

    async def connect(self):
        """
        Handle the connection request.
        """
        # Get the room code from the URL route
        self.room_code = self.scope["url_route"]["kwargs"]["room_code"]
        # Create a unique group name for the room
        self.room_group_name = f"call_{self.room_code}"

        # Join the room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        # Accept the WebSocket connection
        await self.accept()

    async def disconnect(self, close_code):
        """
        Handle the disconnection request.
        """
        # Leave the room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data: str = None, bytes_data: bytes = None):
        """
        Handle incoming messages from the WebSocket.
        """
        # Parse the incoming message
        data = json.loads(text_data)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "send.sdp",
                "data": data,
            },
        )

    async def send_sdp(self, event):
        """
        Send the SDP data to the WebSocket.
        """
        # Get the SDP data from the event
        data = event["data"]

        # Send the SDP data to the WebSocket
        await self.send(text_data=json.dumps(data))


# SDP stands for Session Description Protocol, which is used in WebRTC to describe multimedia communication sessions. It contains information about the media formats, codecs, and network information required to establish a connection.

# WebRTC (Web Real-Time Communication) is a technology that enables peer-to-peer communication between web browsers and mobile applications. It allows audio, video, and data sharing without the need for plugins or third-party software.

# consumers are basically websocket version of views in Django, they handle the websocket connections and messages (receive, send, connect, disconnect).
