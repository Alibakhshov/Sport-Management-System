from django.urls import path
from .views import player_list

urlpatterns = [
    path('players/', player_list, name='player_list'),
    
]
