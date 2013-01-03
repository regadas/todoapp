import uuid
from cal.models import Calendar
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    calendar = models.OneToOneField(Calendar, null=True)
    api_key = models.CharField(max_length=32, default=uuid.uuid1().hex)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        cal = Calendar.objects.create()
        UserProfile.objects.create(user=instance, calendar=cal)

post_save.connect(create_user_profile, sender=User)
