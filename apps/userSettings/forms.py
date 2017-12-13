from django import forms
from apps.user.models import User

class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['mail','visibility_mail', 'company', 'visibility_company','info','visibility_info']
