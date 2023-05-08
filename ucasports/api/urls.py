from django.urls import path
from .views import SportAPIView, TeamAPIView, UserAPIView, CompetitorsAPIView, CompetitionAPIView, EventAPIView, CustomUserDetail, TeamDetail

urlpatterns = [
    path('sports/', SportAPIView.as_view(), name="api_sports"),
    path('teams/', TeamAPIView.as_view(), name="api_teams"),
    path('users/', UserAPIView.as_view(), name="api_users"),
    path('events/', EventAPIView.as_view(), name="api_events"),
    
    path('user/<int:pk>/', CustomUserDetail.as_view(), name='customuser-detail'),
    path('team/<int:pk>/', TeamDetail.as_view(), name='team-detail'),
    
    path('competitions/', CompetitionAPIView.as_view(), name="api_competitions"),
    path('competitors/', CompetitorsAPIView.as_view(), name='api_competitors'),
]