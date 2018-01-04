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
from django.test import TestCase

from .models import User

class UserTestCase(TestCase):
    """ Test cases for the user manager.
    """

    def test_create_active_superuser(self):
        """ Tests if a new created superuser is active.
        """
        User.objects.create_superuser('Test', 'test@test.com', 'Test')
        user = User.objects.get(username='Test')
        self.assertTrue(user.is_staff, msg='Superuser is not a valid staff member.')
        self.assertTrue(user.is_active, msg='Superuser is not set to active.')
        self.assertTrue(user.is_superuser, msg='The Superuser is not a valid superuser.')
        self.assertEqual(user.username, 'Test', msg='The superuser username is not the given name.')
        self.assertEqual(
            user.email,
            'test@test.com',
            msg='The superuser email is not the given email'
        )
        self.assertNotEqual(user.password, 'Test', msg='The superuser password is not hashed.')

    def test_create_user_is_not_active(self):
        """ Tests if a new created user is not active.
        """
        User.objects.create_user('Test', 'test@test.com', 'Test')
        user = User.objects.get(username='Test')
        self.assertFalse(user.is_staff, msg='User is a valid staff member.')
        self.assertFalse(user.is_active, msg='User is set to active.')
        self.assertFalse(user.is_superuser, msg='User is a valid superuser.')
        self.assertEqual(user.username, 'Test', msg='Username is not the given name.')
        self.assertEqual(
            user.email,
            'test@test.com',
            msg='Email is not the given email.'
        )
        self.assertNotEqual(user.password, 'Test', msg='Password is not hashed.')