from django.contrib import admin

from .models import Student, Sport, Team, StudentTeam, Rating, Competition, CompetitionTeam

admin.site.register(Student)
admin.site.register(Sport)
admin.site.register(Team)
admin.site.register(StudentTeam)
admin.site.register(Rating)
admin.site.register(Competition)
admin.site.register(CompetitionTeam)
    
