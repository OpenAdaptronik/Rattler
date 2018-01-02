import os
from django.db import models
from django.conf import settings


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, )
    company = models.CharField(max_length=255, null=True, blank=True)
    info = models.CharField(max_length=255, null=True, blank=True)
    expert = models.BooleanField(default=False)
    visibility_mail = models.BooleanField(default=False)
    visibility_company = models.BooleanField(default=False)
    visibility_info = models.BooleanField(default=False)
    max_projects = models.IntegerField(default=5)
    max_datarows = models.IntegerField(default=1000)
    created = models.DateTimeField
    updated = models.DateTimeField


def profile_image_path(instance, filename):
    return 'profile/%s%s' % (instance.profile.id, os.path.splitext(filename)[1])

class ProfileImage(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    path = models.ImageField(upload_to=profile_image_path)
    created = models.DateTimeField(auto_now_add=True)
updated = models.DateTimeField(auto_now=True)