
from django.shortcuts import render
from .models import Student, Sport, Team, StudentTeam, Rating, Competition, CompetitionTeam

# def player_list(request):
#     players = Player.objects.all()
#     context = {'players': players}
#     return render(request, 'player/player_list.html', context)

def home(request):
    return render(request, 'home.html')

def student_list(request):
    students = Student.objects.all()
    return render(request, '01 - Student_List/student_list.html', {'students': students})

def sport_list(request):
    sports = Sport.objects.all()
    return render(request, '02 - Sport_List/sport_list.html', {'sports': sports})

def team_list(request):
    teams = Team.objects.all()
    return render(request, '03 - Team_List/team_list.html', {'teams': teams})

def student_team_list(request):
    student_teams = StudentTeam.objects.all()
    return render(request, '04 - Student_Team_List/student_team_list.html', {'student_teams': student_teams})

def rating_list(request):
    ratings = Rating.objects.all()
    return render(request, '05 - Rating_List/rating_list.html', {'ratings': ratings})

def competition_list(request):
    competitions = Competition.objects.all()
    return render(request, '06 - Competition_List/competition_list.html', {'competitions': competitions})

def competition_team_list(request):
    competition_teams = CompetitionTeam.objects.all()
    return render(request, '07 - Compitition_Team_List/competition_team_list.html', {'competition_teams': competition_teams})

