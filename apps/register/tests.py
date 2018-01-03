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

from unittest.mock import patch, PropertyMock, sentinel

from django.test import TestCase
from django.contrib.auth.backends import ModelBackend as django_ModelBackend

from .auth import UsernameEmailAuthBackend, UserModel

class RegisterAuthTestCase(TestCase):
    """ Test cases of the auth module.
    """
    def setUp(self):
        """ Sets up the testcase
        """
        self.backend = UsernameEmailAuthBackend()

    @patch('django.contrib.auth.backends.ModelBackend.authenticate')
    def test_call_super_authenticate(self, django_model):
        request = sentinel.some_object
        self.backend.authenticate(request, username='Test', password='test')
        self.assertTrue(django_model.called)
        django_model.assert_called_once_with(request, password='test', username='Test')

    @patch('django.contrib.auth.backends.ModelBackend.authenticate')
    def test_call_super_with_username(self, auth_mock):
        request = sentinel.some_object
        self.backend.authenticate(request, username='Test', password='test')
        self.assertEqual(UserModel.USERNAME_FIELD, 'username')

    @patch('django.contrib.auth.backends.ModelBackend.authenticate')
    def test_call_super_with_email(self, auth_mock):
        request = sentinel.some_object
        self.backend.authenticate(request, username='test@test.de', password='test')
        self.assertEqual(UserModel.USERNAME_FIELD, 'username')

class RegisterTestCase(TestCase):
    """ Test cases of the refister app.
    """
    pass
