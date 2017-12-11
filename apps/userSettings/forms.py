from django import forms
from apps.user.models import User

class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['company', 'info']
