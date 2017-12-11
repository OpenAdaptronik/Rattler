from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from rattler.forms import BaseForm

class RegisterForm(UserCreationForm, BaseForm):
    class Meta:
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ('mail', 'password1', 'password2')

