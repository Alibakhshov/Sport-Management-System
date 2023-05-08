from rest_framework import generics
from rest_framework.response import Response
from ..models import Sport, Team, CustomUser, Competition, Event
from .serializers import SportSerializer, TeamSerializer, CustomUserSerializer, CompetitionSerializer, EventSerializer
from rest_framework.permissions import IsAuthenticated

class CompetitionAPIView(generics.ListAPIView):
    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializer
    permission_classes = [IsAuthenticated]

class SportAPIView(generics.ListAPIView):
    queryset = Sport.objects.all()
    serializer_class = SportSerializer
    permission_classes = [IsAuthenticated]

class TeamAPIView(generics.ListAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]

class UserAPIView(generics.ListAPIView):
    queryset = CustomUser.objects.filter(is_superuser=False, is_staff=False)
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]
    
class EventAPIView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]
    
    
class CompetitorsAPIView(generics.ListAPIView):
    def get_queryset(self):
        sport_id = self.request.query_params.get('sport_id')
        sport = Sport.objects.get(id=sport_id)

        if sport.sport_type == 'Single-Player':
            queryset = CustomUser.objects.filter(is_superuser=False, is_staff=False)
        else:  # Team-Player
            queryset = Team.objects.filter(sport=sport)
        return queryset

    def get_serializer_class(self):
        sport_id = self.request.query_params.get('sport_id')
        sport = Sport.objects.get(id=sport_id)

        if sport.sport_type == 'Single-Player':
            return CustomUserSerializer
        else:  # Team-Player
            return TeamSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    

class CustomUserDetail(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class TeamDetail(generics.RetrieveAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer