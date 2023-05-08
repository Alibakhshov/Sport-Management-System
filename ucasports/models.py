from django.db import models
from django.contrib import admin

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager

from datetime import datetime, timedelta

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not username:
            raise ValueError('The Username field must be set')
        if not name:
            raise ValueError('The Name field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, name, password, **extra_fields)
    



class CustomUser(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    bio = models.TextField(null=True, blank=True)
    avatar = models.ImageField(null=True, default="avatar.jpg")
    
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    rating_points = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'name']
    
    def __str__(self):
        return self.name
    


class Sport(models.Model):
    SPORT_TYPE_CHOICES = (
        ('Single-Player', 'Single-Player'),
        ('Team-Player', 'Team-Player'),
    )

    name = models.CharField(max_length=100)
    sport_type = models.CharField(max_length=20, choices=SPORT_TYPE_CHOICES, default='Single-Player')

    def __str__(self):
        return self.name
    

    
class Team(models.Model):
    name = models.CharField(max_length=100)
    avatar = models.ImageField(null=True, default="team_avatar.jpg")
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    members = models.ManyToManyField(CustomUser)
    rating_points = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    
    

class Event(models.Model):
    name = models.CharField(max_length=100)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    start_date_time = models.DateTimeField()
    end_date_time = models.DateTimeField()
    location = models.CharField(max_length=200)
    description = models.TextField()
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    participants = models.ManyToManyField(CustomUser, related_name="events_attended", blank=True)
    declined_participants = models.ManyToManyField(CustomUser, related_name="events_declined", blank=True)

    def __str__(self):
        return self.name
    

class Competition(models.Model):
    STATUS_CHOICES = (
        ('Scheduled', 'Scheduled'),
        ('Finished', 'Finished'),
    )

    name = models.CharField(max_length=100)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    start_date_time = models.DateTimeField()
    end_date_time = models.DateTimeField()
    location = models.CharField(max_length=200)
    description = models.TextField()
    side_a = models.CharField(max_length=100)
    side_b = models.CharField(max_length=100)
    side_a_score = models.IntegerField(default=0)
    side_b_score = models.IntegerField(default=0)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Scheduled')

    def __str__(self):
        return self.name
    
    @property
    def side_a_name(self):
        if self.sport.sport_type == 'Single-Player':
            user = CustomUser.objects.get(pk=self.side_a)
            return user.name
        else:
            team = Team.objects.get(pk=self.side_a)
            return team.name

    @property
    def side_b_name(self):
        if self.sport.sport_type == 'Single-Player':
            user = CustomUser.objects.get(pk=self.side_b)
            return user.name
        else:
            team = Team.objects.get(pk=self.side_b)
            return team.name
        
    @property
    def side_a_avatar(self):
        if self.sport.sport_type == 'Single-Player':
            user = CustomUser.objects.get(pk=int(self.side_a))
            return user.avatar.url
        elif self.sport.sport_type == 'Team-Player':
            team = Team.objects.get(pk=int(self.side_a))
            return team.avatar.url

    @property
    def side_b_avatar(self):
        if self.sport.sport_type == 'Single-Player':
            user = CustomUser.objects.get(pk=int(self.side_b))
            return user.avatar.url
        elif self.sport.sport_type == 'Team-Player':
            team = Team.objects.get(pk=int(self.side_b))
            return team.avatar.url


class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    read = models.BooleanField(default=False)
     
    

class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField(max_length=2000)

    def __str__(self):
        return self.email

class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject")
