"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import GameType


class GameTypeView(ViewSet):
    """Level up game types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game type

        Returns:
            Response -- JSON serialized game type
        """
        try:
            game_type = GameType.objects.get(pk=pk) # retrieve single game type
            # 'get' is equivalent to this sql execute:
            # db_cursor.execute("""
            #     select id, label
            #     from levelupapi_gametype
            #     where id = ?""",(pk,)
            # ) 
            serializer = GameTypeSerializer(game_type) # passed to serializer
            return Response(serializer.data) # sends to client as response body (same as _set_headers and wfile.write)
        except GameType.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        game_types = GameType.objects.all()
        # 'all' is equivalent to this sql execute:
        # select *
        # from levelupapi_gametype
        serializer = GameTypeSerializer(game_types, many=True)
        return Response(serializer.data)

class GameTypeSerializer(serializers.ModelSerializer):
    """JSON serializer for game types"""
    class Meta: # Meta class hold the configuration for the serializer
        model = GameType # telling serializer to use GameType Model
        fields = ('id', 'label') # fields to include from model
