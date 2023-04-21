from django.shortcuts import render
from .models import Player

def player_list(request):
    players = Player.objects.all()
    context = {'players': players}
    return render(request, 'player/player_list.html', context)

