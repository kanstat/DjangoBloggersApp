from django.db import models
from django.utils import timezone
# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField()
    session_id = models.CharField(max_length=100, default=0)
    time_stamp = models.DateTimeField(default=timezone.now)
    email_verification = models.BooleanField(default=0)
    read_permission = models.CharField(max_length=50, default='')
    write_permission = models.CharField(max_length=50, default='')


class Tinymce(models.Model):
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)
    content = models.TextField()
    user_fk = models.ForeignKey(User, models.CASCADE, default='')
    title = models.CharField(max_length=200, default='Untitled')
    published_url = models.URLField(default='')
    pub_url_active = models.BooleanField(default=False)
