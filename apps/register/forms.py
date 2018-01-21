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
from django.contrib.auth.forms import UserCreationForm

from rattler.forms import BaseForm
from captcha.fields import ReCaptchaField

class RegisterForm(UserCreationForm, BaseForm):
    """ User registration form.
    Extends the django.contrib.auth.forms.UserCreationForm and rattler.forms.BaseForm.
    """

    captcha = ReCaptchaField()

    class Meta:
        """ Meta informations.
        """
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ('email', 'password1', 'password2')
