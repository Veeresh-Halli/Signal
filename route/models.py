from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class LoggedUsers(models.Model):
    user = models.ForeignKey(User, null=True,on_delete=models.SET_NULL)

    def __str__(self):
        return self.user.username