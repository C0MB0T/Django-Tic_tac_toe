from django.shortcuts import render, redirect, HttpResponse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

import json
from . import models, consumers



def index(request):
    context = {
        'games': models.Game.objects.all()
    }
    return render(request, 'main/index.html', context)


def new(request):
    user = request.COOKIES.get('user')
    game = models.Game.objects.create(
        user1 = user,
    )
    async_to_sync(get_channel_layer().group_send)(
        'chat_Lobby',
            {
                'type': 'chat_message',
                'message': json.dumps({'code': game.code_game, 'user': user, 'type': 'add'})
            }
    )

    return redirect('/game/' + game.code_game)


def game(request, code):
    game = models.Game.objects.filter(code_game=code)
    if game:
        context = {
            'code_game': code,
            'game_user': game[0].user1,
        }
        return render(request, 'main/game.html', context)
    else:
        return redirect('/')


def join(request, code):
    game = models.Game.objects.filter(code_game=code)
    if game:
        game = game[0]
        if game.user2:
            return redirect('/')
        else:
            game.user2 = request.COOKIES.get('user')
            game.save()
            async_to_sync(get_channel_layer().group_send)(
                'chat_Lobby',
                    {
                        'type': 'chat_message',
                        'message': json.dumps({'code': game.code_game, 'user': game.user1, 'type': 'remove'})
                    }
            )

            return redirect('/game/' + game.code_game)
    else:
        return redirect('/')
