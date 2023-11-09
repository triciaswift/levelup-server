from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    """Database model for tracking events"""

    name = models.CharField(max_length=200)
    date_time = models.DateTimeField()
    location = models.CharField(max_length=200)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="organized_events")
    game = models.ForeignKey("Game", on_delete=models.CASCADE, related_name="events")
    attendees = models.ManyToManyField(User, through="EventGamer", related_name="attending_events")
