from django import forms
from . import models

class ProfileForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = ['company', 'info', 'expert', 'visibility_mail', 'visibility_company', 'visibility_info']

class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = models.ProfileImage
        fields = ['path']


ProfileImageFormSet = forms.inlineformset_factory(
    models.Profile,
    models.ProfileImage,
    fk_name='profile',
    form=ProfileImageForm,
    extra=1,
    fields=('path',)
)