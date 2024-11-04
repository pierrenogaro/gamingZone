from django.db import models
from django.contrib.auth.models import User

class Cemantix(models.Model):
    word = models.CharField(max_length=100)
    similarity = models.FloatField(null=True, blank=True)

class Hangman(models.Model):
    solution = models.CharField(max_length=100)
    guesse_letter = models.TextField()

class Lock(models.Model):
    lock_code = models.CharField(max_length=4)

class Score(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}: {self.points}"