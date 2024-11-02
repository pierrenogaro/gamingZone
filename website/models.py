from django.db import models

class Guess(models.Model):
    word = models.CharField(max_length=100)
    similarity = models.FloatField(null=True, blank=True)
