from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    nickname = models.CharField(max_length=20, blank=True)
    participant = models.ManyToManyField('Meeting', blank=True, related_name='participant')  # 참가자


class Meeting(models.Model):
    proponent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='proponent')  # 제안자
    meet_date = models.DateTimeField(blank=False)
    meet_title = models.CharField(max_length=200, blank=True)
    meet_desc = models.CharField(max_length=500)
    created_date = models.DateTimeField(default=timezone.now)
    participants = models.CharField(max_length=20)
    participant_count = models.PositiveIntegerField(default=0)

