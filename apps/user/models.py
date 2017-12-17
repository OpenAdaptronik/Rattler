from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

from django.contrib.auth.models import User
from django.core.mail import send_mail

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            mail=self.normalize_email(email),
            username=username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            mail=self.normalize_email(email),
            username=username,
            password=password
        )
        user.is_active = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    mail = models.EmailField(unique=True)
    username = models.CharField(max_length=255, unique=True, default=None)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created = models.DateTimeField
    updated = models.DateTimeField

    USERNAME_FIELD = 'mail'
    EMAIL_FIELD = 'mail'

    objects = UserManager()

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Sends an EMail to the User

        Sends an email to the user mail address. Uses the django internal mail system.

        Arguments:
            subject {string} -- The mail subject
            message {string} -- The mail message
            **kwargs {[type]} -- [description]

        Keyword Arguments:
            from_email {tuple|list} -- [description] (default: {None})
        """

        send_mail(subject, message, from_email, [self.mail], **kwargs)
