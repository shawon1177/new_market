from django.db import models
from django.conf import settings


# Create your models here.

class Conversation(models.Model):
    users = models.ManyToManyField(settings.AUTH_USER_MODEL)

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)    