from django.utils import timezone
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async, async_to_sync
from .models import TravelMate
from helper.Constants import ONLINE, OFFLINE, LAST_SEEN
import humanize

class TravelMateStatusConsumer(AsyncJsonWebsocketConsumer):
    groups = []

    async def connect(self):
        # authentication
        if self.scope['travel_mate'] is not None and self.scope['done']:
            self.travel_mate = self.scope['travel_mate']
            await self.channel_layer.group_add('server', self.channel_name)
            await self.accept()
            await self.change_travel_mate_status_to_online()
            await self.channel_layer.group_send('server', {
                'type': 'send_travel_mate_status',
                'data': await self.get_all_travel_mate_status_data(),
            })
        else:
            print(self.scope['msg'])
            self.travel_mate = None
            await self.close()

    async def receive_json(self, content, **kwargs):
        pass

    @database_sync_to_async
    def get_all_travel_mate_status_data(self):
        statuses = list(TravelMate.objects.order_by('-is_online').values('travel_mate_id', 'is_online'))
        return statuses
    async def disconnect(self, close_code):
        if self.travel_mate is not None:
            await self.channel_layer.group_discard('server', self.channel_name)
            await self.change_travel_mate_status_to_offline()
            await self.channel_layer.group_send('server', {
                'type': 'send_travel_mate_status',
                'data': await self.get_all_travel_mate_status_data(),
            })
        print('websocket disconnect')

    async def send_travel_mate_status(self,event):
        await self.send_json(content = event['data'])


    @database_sync_to_async
    def change_travel_mate_status_to_online(self):
        travel_mate = self.travel_mate
        travel_mate.is_online = True
        travel_mate.save()

    @database_sync_to_async
    def change_travel_mate_status_to_offline(self):
        travel_mate = self.travel_mate
        travel_mate.is_online = False
        travel_mate.save()
