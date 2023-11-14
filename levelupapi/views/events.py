"""View module for handling requests about events"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event
from django.contrib.auth.models import User
    

class EventView(ViewSet):
    """Level up events view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single event
        
        Returns -- JSON serialized event
        """

        try:
            event = Event.objects.get(pk=pk)
            serializer = EventSerializer(event)
            return Response(serializer.data)
        except Event.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all events

        Returns:
            Response -- JSON serialized list of events
        """
        # Get query string parameter
        game_only = self.request.query_params.get("game", None)

        try:
            # Start with all rows
            events = Event.objects.all()
            if game_only is not None:
                try:
                    # If game_only='num' then convert to an integer
                    game_id = int(game_only)
                    # Filter the queryset based on game parameter
                    events = events.filter(game=game_id)
                except ValueError:
                    return Response({"error": "Invalid game id"}, status=status.HTTP_400_BAD_REQUEST)
            serializer = EventSerializer(events, many=True)
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)



class EventOrganizerSerializer(serializers.ModelSerializer):
    """JSON serializer for event organizers"""
    full_name = serializers.SerializerMethodField()

    def get_full_name(self, obj):
        return f'{obj.first_name} {obj.last_name}'

    class Meta:
        model = User
        fields = ('id', 'full_name')


class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for events"""

    date = serializers.SerializerMethodField()
    time = serializers.SerializerMethodField()
    organizer = EventOrganizerSerializer(many=False)
    attendees = EventOrganizerSerializer(many=True)

    def get_date(self, obj):
        return obj.date_time.date().strftime("%Y-%m-%d")

    def get_time(self, obj):
        return obj.date_time.time().strftime("%I:%M %p")


    class Meta:
        model = Event
        fields = ('id', 'name', 'date', 'time', 'organizer', 'game', 'attendees')
