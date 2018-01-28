from django.contrib.auth.forms import AuthenticationForm as auth_AuthenticationForm
from apps.register.forms import RegisterForm as real_RegisterForm


class AuthenticationForm(auth_AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(AuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.pop("autofocus", None)
class RegisterForm(real_RegisterForm):
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.pop("autofocus", None)
