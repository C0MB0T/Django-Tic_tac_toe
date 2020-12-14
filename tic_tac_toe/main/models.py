from django.db import models
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
import uuid 


def get_code():
    return str(uuid.uuid4())[:6]

class Game(models.Model):
    code_game = models.CharField(max_length=6, default=get_code)
    user1 = models.CharField(max_length=100, null=True)
    user2 = models.CharField(max_length=100, null=True)
    game_stats = models.CharField(max_length=50, null=True)

    def delete(self, *args, **kwargs):
        async_to_sync(get_channel_layer().group_send)(
            'chat_Lobby',
                {
                    'type': 'chat_message',
                    'message': json.dumps({'code': self.code_game, 'user': self.user1, 'type': 'remove'})
                }
        )
        super(Game, self).delete(*args, **kwargs)


    