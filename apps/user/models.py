from django.db import models
from django.contrib.auth.models import (AbstractUser, UserManager as auth_UserManager)
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import User
from django.core.mail import send_mail

class UserManager(auth_UserManager):
    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_active', True)
        return super(UserManager, self).create_superuser(username, email, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(_('email address'))
    is_active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = UserManager()
