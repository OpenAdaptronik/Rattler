from django import forms
from apps.user.models import User

class userSettingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['mail', ]
