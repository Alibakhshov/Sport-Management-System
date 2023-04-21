from django.db import models

class Student(models.Model):
    student_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    faculty = models.CharField(max_length=255)
    birth_date = models.DateField()
    email = models.EmailField(unique=True)
    course = models.CharField(max_length=255)
    
    def __str__(self):
        return self.first_name + ' ' + self.last_name

class Sport(models.Model):
    sport_id = models.AutoField(primary_key=True)
    sport_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.sport_name

class Team(models.Model):
    team_id = models.AutoField(primary_key=True)
    team_name = models.CharField(max_length=255)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.team_name
    

class StudentTeam(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null=True)
    position = models.CharField(max_length=255)
    
    def __str__(self):
        return self.student.first_name + ' ' + self.student.last_name + ' - ' + self.team.team_name
    
    class Meta:
        # Define a unique constraint for student and team combination
        unique_together = ('student', 'team')

class Rating(models.Model):
    rating_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    rating = models.IntegerField()
    
    def __str__(self):
        return self.student.first_name + ' ' + self.student.last_name + ' - ' + self.team.team_name + ' - ' + str(self.rating)

class Competition(models.Model):
    competition_id = models.AutoField(primary_key=True)
    competition_name = models.CharField(max_length=255)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    location = models.CharField(max_length=255)
    
    def __str__(self):
        return self.competition_name + ' - ' + self.sport.sport_name

class CompetitionTeam(models.Model):
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    position = models.IntegerField()
    
    def __str__(self):
        return self.competition.competition_name + ' - ' + self.team.team_name + ' - ' + str(self.position)

    class Meta:
        # Define a unique constraint for competition and team combination
        unique_together = ('competition', 'team')
