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

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

# pylint: disable=C0103
UserModel = get_user_model()

class UsernameEmailAuthBackend(ModelBackend):
    """ Authenticate the user with the given username or email.
    Overwrites the default auth backend django.contrib.auth.backends.ModelBackend.
    Detects if the username is an email if the username contains an '@'.

    Attributes:
        See django.contrib.auth.backends.ModelBackend.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        """ Authenticate a user by username or email and password.
        Uses the user email if the username contains an '@'.

        Args:
            username: The username or the user email. Detect automaticly if
                the username is an email, if it contains an '@'.
            password: The user password.

        Returns:
            The authenticated user or None if not valid.
        """
        if '@' in username:
            UserModel.USERNAME_FIELD = 'email'
        else:
            UserModel.USERNAME_FIELD = 'username'

        user = super(UsernameEmailAuthBackend, self).authenticate(
            request,
            username=username,
            password=password,
            **kwargs
        )

        UserModel.USERNAME_FIELD = 'username'
        return user
