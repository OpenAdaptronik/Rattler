import os
from django.db import models
from django.conf import settings


from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, )
    company = models.CharField(max_length=255, null=True, blank=True)
    info = models.CharField(max_length=255, null=True, blank=True)
    expert = models.BooleanField(default=False)
    visibility_mail = models.BooleanField(default=False)
    visibility_company = models.BooleanField(default=False)
    visibility_info = models.BooleanField(default=False)
    visibility_first_name = models.BooleanField(default=False)
    visibility_last_name = models.BooleanField(default=False)
    max_projects = models.IntegerField(default=5)
    max_datarows = models.IntegerField(default=1000)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')

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
