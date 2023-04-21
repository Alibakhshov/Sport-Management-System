from django.urls import path
from .views import home, student_list, sport_list, team_list, student_team_list, rating_list, competition_list, competition_team_list

# app_name = 'students'

urlpatterns = [
    path('', home, name='home'),
    path('students/', student_list, name='student_list'),
    path('sports/', sport_list, name='sport_list'),
    path('teams/', team_list, name='team_list'),
    path('student-teams/', student_team_list, name='student_team_list'),
    path('ratings/', rating_list, name='rating_list'),
    path('competitions/', competition_list, name='competition_list'),
    path('competition-teams/', competition_team_list, name='competition_team_list'),
]

