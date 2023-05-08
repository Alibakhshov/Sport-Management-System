from rest_framework import serializers
from ..models import Sport, Team, CustomUser, Competition, Event

class SportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sport
        fields = ('id', 'name', 'sport_type')

class TeamSerializer(serializers.ModelSerializer):
    sport = SportSerializer(read_only=True)
    
    class Meta:
        model = Team
        fields = ('id', 'name', 'sport', 'avatar', 'rating_points', 'wins', 'losses')

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'name', 'email', 'avatar', 'rating_points')
        
class CreatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['name']
        
class EventSerializer(serializers.ModelSerializer):
    sport = SportSerializer(read_only=True)
    event_type = serializers.CharField(default='Event')
    
    creator = CreatorSerializer()
    participants_count = serializers.IntegerField(source='participants.count')
    declined_participants_count = serializers.IntegerField(source='declined_participants.count')

    class Meta:
        model = Event
        fields = ('id', 'name', 'sport', 'start_date_time', 'end_date_time', 'location', 'description', 'participants_count', 'declined_participants_count', 'creator', 'event_type')
            
        
class CompetitionSerializer(serializers.ModelSerializer):
    sport = SportSerializer(read_only=True)
    event_type = serializers.CharField(default='Competition')

    class Meta:
        model = Competition
        fields = ('id', 'name', 'sport', 'start_date_time', 'end_date_time', 'side_a', 'side_b', 'side_a_score', 'side_b_score', 'location', 'description', 'status', 'event_type')