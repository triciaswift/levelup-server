"""View module for handling requests about events"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event, Game
from django.contrib.auth.models import User
from django.utils.dateparse import parse_datetime
from datetime import datetime
    

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
        game_id = self.request.query_params.get("game", None)

        try:
            # Start with all rows
            events = Event.objects.all()
            if game_id is not None:
                try:
                    # Filter the queryset based on game parameter
                    events = events.filter(game=game_id)
                except ValueError:
                    return Response({"error": "Invalid game id"}, status=status.HTTP_400_BAD_REQUEST)
            serializer = EventSerializer(events, many=True)
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
        
    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """
        event_date = request.data.get("date")
        event_time = request.data.get("time")

        # Convert time from 12-hour format with AM/PM to 24-hour format
        time_obj = datetime.strptime(event_time, '%I:%M %p').time()

        # Combine date & time into datetime object
        event_datetime = f'{event_date} {time_obj}'

        name = request.data.get("name")
        # Using parse_datetime
        parsed_datetime = parse_datetime(event_datetime)
        location = request.data.get("location")
        game_name = Game.objects.get(pk=request.data["game"])

        # Use the create() method shortcut or the imperative approach.
        event = Event.objects.create(
            name=name,
            date_time=parsed_datetime,
            location=location,
            organizer=request.user,
            game=game_name,
        )

        # Serialize the data and send it back to the client
        serializer = EventSerializer(event, context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class EventOrganizerSerializer(serializers.ModelSerializer):
    """JSON serializer for event organizers"""
    full_name = serializers.SerializerMethodField()

    def get_full_name(self, obj):
        return f'{obj.first_name} {obj.last_name}'

    class Meta:
        model = User
        fields = ('id', 'full_name')

class EventGameSerializer(serializers.ModelSerializer):
    """JSON serializer for event games"""

    class Meta:
        model = Game
        fields = ('id', 'name')


class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for events"""

    date = serializers.SerializerMethodField()
    time = serializers.SerializerMethodField()
    organizer = EventOrganizerSerializer(many=False)
    game = EventGameSerializer(many=False)
    attendees = EventOrganizerSerializer(many=True)

    def get_date(self, obj):
        return obj.date_time.date().strftime("%Y-%m-%d")

    def get_time(self, obj):
        return obj.date_time.time().strftime("%I:%M %p")


    class Meta:
        model = Event
        fields = ('id', 'name', 'date', 'time', 'location', 'organizer', 'game', 'attendees')
