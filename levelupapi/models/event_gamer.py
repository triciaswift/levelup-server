from django.db import models
from django.contrib.auth.models import User

class EventGamer(models.Model):
    """Database model for tracking Gamer Events"""

    event = models.ForeignKey("Event", on_delete=models.CASCADE)
    attendee = models.ForeignKey(User, on_delete=models.CASCADE)