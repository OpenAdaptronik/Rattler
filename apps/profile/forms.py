from django.forms import ModelForm
from . import models

class ProfileForm(ModelForm):
    class Meta:
        model = models.Profile
        fields = ['company', 'info', 'expert', 'visibility_mail', 'visibility_company', 'visibility_info']