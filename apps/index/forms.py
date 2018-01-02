from django.contrib.auth.forms import AuthenticationForm as auth_AuthenticationForm


class AuthenticationForm(auth_AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(AuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.pop("autofocus", None)
