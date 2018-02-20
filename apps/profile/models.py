import os
from django.db import models
from django.conf import settings

from django.utils.translation import gettext_lazy as _

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('user') )
    company = models.CharField(_('company'),max_length=255, null=True, blank=True)
    info = models.CharField(_('info'),max_length=255, null=True, blank=True)
    expert = models.BooleanField(_('expert'),default=False)
    visibility_mail = models.BooleanField(_('visibility of mail adress'),default=False)
    visibility_company = models.BooleanField(_('visibility of company'),default=False)
    visibility_info = models.BooleanField(_('visibility of information'),default=False)
    visibility_first_name = models.BooleanField(_('visibility of first name'),default=False)
    visibility_last_name = models.BooleanField(_('visibility of last name'), default=False)
    max_projects = models.IntegerField(_('maximum number of projects'),default=5)
    max_datarows = models.IntegerField(_('maximum number of datarows'), default=10000)
    created = models.DateTimeField(_('created'),auto_now_add=True)
    updated = models.DateTimeField(_('updated'),auto_now=True)

    def __str__(self):
        return _('%(username)s profile') % {'username': self.user.username}



def profile_image_path(instance, filename):
    return 'profile/%s%s' % (instance.profile.id, os.path.splitext(filename)[1])

class ProfileImage(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, verbose_name=_('profile'))
    path = models.ImageField(_('path'),upload_to=profile_image_path)
    created = models.DateTimeField(_('created'),auto_now_add=True)
    updated = models.DateTimeField(_('updated'),auto_now=True)

    class Meta:
        verbose_name = _('profile image')
        verbose_name_plural = _('profile images')

@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=get_user_model())
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
