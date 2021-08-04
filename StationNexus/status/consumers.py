from channels.generic.websocket import AsyncWebsocketConsumer
import json
from datetime import datetime


class DataConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("Consumer CONNECT")
        self.room_name = self.scope["url_route"]["kwargs"]["view_station"]
        self.room_group_name = "data_%s" % self.room_name
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def send_data(self, event):
        print("Consumer SEND_DATA")
        data = {}
        data["test_msg"] = "Test msg"
        data["test_time"] = str(datetime.now().time())

        await self.send(text_data=json.dumps({"message": data}))
