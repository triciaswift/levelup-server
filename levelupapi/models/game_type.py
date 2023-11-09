from django.db import models

class GameType(models.Model):
    """Database model for tracking game types"""

    label = models.CharField(max_length=200)