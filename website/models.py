from django.db import models

class Guess(models.Model):
    word = models.CharField(max_length=100)
