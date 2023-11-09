from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
    """Database for tracking games"""

    name = models.CharField(max_length=200)
    manufacturer = models.CharField(max_length=200)
    number_of_players = models.IntegerField()
    type = models.ForeignKey("GameType", on_delete=models.CASCADE, related_name="games")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="games")