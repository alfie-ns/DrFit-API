from django.db import models
from django.contrib.auth.models import User

# Create your models here.


def get_default_history():
    return []

class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    history = models.JSONField(default=get_default_history)

    def __str__(self):
        return f"Conversation of {self.user}"
