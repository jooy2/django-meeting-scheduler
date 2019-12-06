from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django_summernote import models as summer_model
from django_summernote import fields as summer_fields


class User(AbstractUser):
    nickname = models.CharField(max_length=20, blank=True)


class Meeting(summer_model.Attachment):
    proponent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='proponent')  # 제안자
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=False, related_name='participants')  # 참가자
    meet_date = models.DateTimeField(blank=False)
    meet_title = models.CharField(max_length=200, blank=True)
    meet_desc = models.CharField(max_length=500)
    meet_contents = summer_fields.SummernoteTextField(default='')
    created_date = models.DateTimeField(default=timezone.now)
    progress = models.BooleanField(default=False)


class Comment(models.Model):
    meet_schedule = models.ForeignKey('Meeting', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=20)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text
