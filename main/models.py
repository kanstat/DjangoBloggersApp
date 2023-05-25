from django.db import models
from django.utils import timezone
# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=30)
    email = models.EmailField()
    session_id = models.CharField(max_length=100, default=0)
    time_stamp = models.DateTimeField(default=timezone.now)
    email_verification = models.BooleanField(default=0)
