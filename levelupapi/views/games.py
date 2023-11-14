"""View module for handling requests about games"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Game, GameType
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
            serializer = GameSerializer(game)
            return Response(serializer.data)
        except Game.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all games

        Returns:
            Response -- JSON serialized list of games
        """

        games = Game.objects.all()
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """
        name = request.data.get("name")
        manufacturer = request.data.get("manufacturer")
        number_of_players = request.data.get("number_of_players")
        game_type = GameType.objects.get(pk=request.data["type"])

        # Use the create() method shortcut or the imperative approach.
        game = Game.objects.create(
            name=name,
            manufacturer=manufacturer,
            number_of_players=number_of_players,
            type=game_type,
            creator=request.user,
        )

        # Serialize the data and send it back to the client
        serializer = GameSerializer(game, context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class GameCreatorSerializer(serializers.ModelSerializer):
    """JSON serializer for game organizers"""
    full_name = serializers.SerializerMethodField()

    def get_full_name(self, obj):
        return f'{obj.first_name} {obj.last_name}'

    class Meta:
        model = User
        fields = ('id', 'full_name')


class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for games"""

    creator = GameCreatorSerializer(many=False)
    type = GameTypeSerializer(many=False)

    class Meta:
        model = Game
        fields = ('id', 'name', 'manufacturer', 'number_of_players', 'type', 'creator')
