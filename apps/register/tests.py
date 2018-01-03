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

from unittest.mock import patch, sentinel, Mock

from django.test import TestCase

from .auth import UsernameEmailAuthBackend, UserModel
from . import tokens

class RegisterAuthTestCase(TestCase):
    """ Test cases of the auth module.
    """
    def setUp(self):
        """ Sets up the testcase
        """
        self.backend = UsernameEmailAuthBackend()

    @patch('django.contrib.auth.backends.ModelBackend.authenticate')
    def test_call_super_authenticate(self, auth_mock):
        """ Test if the super method authenticate was called.
        """
        request = sentinel.some_object
        self.backend.authenticate(request, username='Test', password='test')
        self.assertTrue(auth_mock.called)
        auth_mock.assert_called_once_with(request, password='test', username='Test')

    @patch('django.contrib.auth.backends.ModelBackend.authenticate')
    def test_call_super_with_username(self, auth_mock):
        """ Test if the super with username.
        """
        request = sentinel.some_object
        self.backend.authenticate(request, username='Test', password='test')
        self.assertEqual(UserModel.USERNAME_FIELD, 'username')
        auth_mock.assert_called_once_with(request, password='test', username='Test')

    @patch('django.contrib.auth.backends.ModelBackend.authenticate')
    def test_call_super_with_email(self, auth_mock):
        """ Test if the super with email.
        """
        request = sentinel.some_object
        self.backend.authenticate(request, username='test@test.de', password='test')
        self.assertEqual(UserModel.USERNAME_FIELD, 'username')
        auth_mock.assert_called_once_with(request, password='test', username='test@test.de')

class AccountActivationTokenGeneratorTestCase(TestCase):
    """ Test cases for AccountActivationTokenGenerator
    """
    def test_instance(self):
        """ Test if account_activation_token is an instance of AccountActivationTokenGenerator
        """
        self.assertIsInstance(
            tokens.account_activation_token,
            tokens.AccountActivationTokenGenerator
        )

    def test__make_hash_value(self):
        """ Test method _make_hash_value
        """
        user = Mock(id=1, is_active=False, email='test@test.de')
        # pylint: disable=W0212
        self.assertEqual(
            tokens.account_activation_token._make_hash_value(user, 12),
            '112Falsetest@test.de'
        )
        user = Mock(id=532, is_active=True, email='rattler@test.de')
        # pylint: disable=W0212
        self.assertEqual(
            tokens.account_activation_token._make_hash_value(user, 421),
            '532421Truerattler@test.de'
        )

class RegisterTestCase(TestCase):
    """ Test cases of the register app.
    """
    pass
