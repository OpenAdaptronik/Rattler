from django import forms
from apps.profile.models import Profile


class UserSettings(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['company', 'info', 'visibility_info', 'visibility_company',
                  'visibility_mail', 'expert']
