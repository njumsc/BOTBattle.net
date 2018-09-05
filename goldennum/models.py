from django.db import models

# Create your models here.

class Room(models.Model):
    roomid = models.CharField(max_length=100)
    time = models.IntegerField()
    history = models.CharField(max_length=1000)
    cmd_run = models.CharField(max_length=200)
    cmd_kill = models.CharField(max_length=200)

    def __str__(self):
        return self.roomid

class User(models.Model):
    name = models.CharField(max_length=100)
    room = models.CharField(max_length=100)
    score = models.IntegerField()
    act1 = models.FloatField()
    act2 = models.FloatField()

    def __str__(self):
        return self.name
