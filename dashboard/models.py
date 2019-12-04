from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    nickname = models.CharField(max_length=20, blank=True)


class Meeting(models.Model):
    proponent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='proponent', blank=False)  # 제안자
    participant = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='participant')  # 참가자
    meetDate = models.DateTimeField(blank=False)
    meetTitle = models.CharField(max_length=200, blank=True)
    meetDesc = models.CharField(max_length=500)
    created_date = models.DateTimeField(default=timezone.now)

