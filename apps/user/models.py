""" License
MIT License

Copyright (c) 2017 OpenAdaptronik

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from django.db import models
from django.contrib.auth.models import (AbstractUser, UserManager as auth_UserManager)
from django.utils.translation import gettext_lazy as _


class UserManager(auth_UserManager):
    """ The User Manager Class.

    Overwrites the default django.contrib.auth.models.UserManager.
    Creates a new superuser with is_active set to true.

    Attributes:
        See django.contrib.auth.models.UserManager
    """
    def create_superuser(self, username, email, password, **extra_fields):
        """ Creates a new superuser.

        Creates a new superuser and sets the is_active to true.

        Args:
            username: The username of the new superuser.
            email: The email of the new superuser.
            password: The cleartext password of the new superuser.
            extra_fields: Additional fields to set to the new superuser.
        """
        extra_fields.setdefault('is_active', True)
        return super(UserManager, self).create_superuser(username, email, password, **extra_fields)

class User(AbstractUser):
    """ The user database model.

    Overwrites the default django.contrib.auth.models.AbstractUser.
    Defines the user and its fields.

    Attributes:
        See django.contrib.auth.models.AbstractUser.
        email: The user email field.
        is_active: The is active flag. Only active useres are allowed to login.
        created: The creation date of the user.
        updated: The last update date of the user.
        objects: The UserManager instance.
    """
    email = models.EmailField(_('email address'))
    is_active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = UserManager()
