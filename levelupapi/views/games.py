"""View module for handling requests about games"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Game
from django.contrib.auth.models import User
from .game_types import GameTypeSerializer


class GameView(ViewSet):
    """Level up games view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game
        
        Returns -- JSON serialized game
        """

        try:
            game = Game.objects.get(pk=pk)
            serializer = EventSerializer(game)
            return Response(serializer.data)
        except Game.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all games

        Returns:
            Response -- JSON serialized list of games
        """

        games = Game.objects.all()
        serializer = EventSerializer(games, many=True)
        return Response(serializer.data)


class EventOrganizerSerializer(serializers.ModelSerializer):
    """JSON serializer for game organizers"""
    full_name = serializers.SerializerMethodField()

    def get_full_name(self, obj):
        return f'{obj.first_name} {obj.last_name}'

    class Meta:
        model = User
        fields = ('id', 'full_name')


class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for games"""

    creator = EventOrganizerSerializer(many=False)
    type = GameTypeSerializer(many=False)

    class Meta:
        model = Game
        fields = ('id', 'name', 'manufacturer', 'number_of_players', 'type', 'creator')
