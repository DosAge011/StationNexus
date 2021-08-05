import json
from channels.generic.websocket import AsyncWebsocketConsumer
from datetime import datetime


class TestConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("STATUS Consumer TEST CONNECT")
        self.room_name = self.scope["url_route"]["kwargs"]["view_station"]
        self.room_group_name = "data_%s" % self.room_name
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def send_test_data(self, event):
        print("STATUS Consumer SEND_TEST_DATA")
        data = {}
        data["test_msg"] = "Test msg"
        data["test_time"] = str(datetime.now().time())

        await self.send(text_data=json.dumps({"message": data}))


class DataConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["view_station"]
        self.room_group_name = "data_%s" % self.room_name

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def send_data(self, event):
        data = {}
        data["active_units"] = str(event["active_units"])
        data["oos_units"] = str(event["oos_units"])
        data["personnel"] = str(event["personnel"])

        await self.send(text_data=json.dumps({"message": data}))
