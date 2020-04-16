from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# With help from https://blog.heroku.com/in_deep_with_django_channels_the_future_of_real_time_apps_in_django
# Create your models here.
class Room(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages',on_delete=models.CASCADE)
    handle = models.TextField()
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)