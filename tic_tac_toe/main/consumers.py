from asgiref.sync import async_to_sync, sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
import json

from . import models


class IndexConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        #self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_name = 'Lobby'
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

wins_list = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],
    [0, 3, 6], [1, 4, 7], [2, 5, 8],
    [0, 4, 8], [2, 4, 6]
]
wins_sets = []
for i in wins_list:
    wins_sets.append(set(i))

class GameConsumer(AsyncWebsocketConsumer):
    @sync_to_async
    def get_game(self):
        return models.Game.objects.get(code_game=self.room_name) 


    @sync_to_async
    def delete_game(self):
        return self.game.delete()


    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        self.game = await self.get_game()

        self.game_history = []

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        #print(self.scope)
        await self.accept()

        context = {
            'type': 'start',
            'user': self.scope['cookies']['user'],
        }
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'context': context,
            }
        )


    async def disconnect(self, close_code):
        # Leave room group
        #self.game.delete()

        await self.delete_game()
        context = {
            'type': 'disconnect',
        }
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'context': context,
            }
        )

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        print(self.room_name)
        text_data_json = json.loads(text_data)

        self.game_history.append(int(text_data_json['ceil']))
        win = False
        for i in wins_sets:
            if i == i & set(self.game_history):
                win = True
        print(self.game_history)
        # Send message to room group
        context = {
            'type': 'turn',
            'win': False,
            'ceil': text_data_json['ceil'],
            'from_user': text_data_json['user'],
        }
        if win:
            context['win'] = True
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'context': context
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        context = event['context']
        await self.send(text_data=json.dumps(context))
    