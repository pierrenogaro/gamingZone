from django.db import models

class Cemantix(models.Model):
    word = models.CharField(max_length=100)
    similarity = models.FloatField(null=True, blank=True)

class Hangman(models.Model):
    solution = models.CharField(max_length=100)
    guesse_letter = models.TextField()


