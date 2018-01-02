import os
from django.db import models
from django.conf import settings


from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model


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


    def curruser_company_finder(self):
        return self.objects.filter(userID=user.id).values['company']

def profile_image_path(instance, filename):
    return 'profile/%s%s' % (instance.profile.id, os.path.splitext(filename)[1])

class ProfileImage(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    path = models.ImageField(upload_to=profile_image_path)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=get_user_model())
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
