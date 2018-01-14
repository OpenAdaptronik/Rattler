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

from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth.models import Group

from django.utils.translation import gettext_lazy as _

from .models import User

# Unregister the default group admin model.
admin.site.unregister(Group)

@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    """ The user admin model.
    Overwrites the default django.contrib.auth.admin.UserAdmin
    Admin model to manipulate the users in the database.

    Attributes:
        See django.contrib.auth.models.AbstractUser.
        fieldsets: The fieldset to show in the admin.
        list_display: The data to show in the user list.
        add_fieldsets: The data to show in the user creation.
    """
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        (_('Permissions'), {'fields': ('is_active', 'is_superuser')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('name'), {'fields': ('last_name', 'first_name')}),
    )

    list_display = ('username', 'email', 'is_superuser','is_active', 'date_joined', 'updated', )
    list_filter = ('is_superuser', 'is_active')
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )



