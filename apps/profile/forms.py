from django import forms
from . import models
from apps.user.models import User

class ProfileForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = ['company', 'info', 'expert', 'visibility_mail',
                  'visibility_company', 'visibility_info',
                  'visibility_first_name','visibility_last_name']

class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = models.ProfileImage
        fields = ['path']

class UserForm(forms.ModelForm):
    class Meta:
        model= User
        fields = ['first_name','last_name']

ProfileImageFormSet = forms.inlineformset_factory(
    models.Profile,
    models.ProfileImage,
    fk_name='profile',
    form=ProfileImageForm,
    extra=1,
    fields=('path',)
)
ProfileFormSet = forms.inlineformset_factory(
    model=models.Profile,
    parent_model=User,
    fk_name='user',
    form=ProfileForm,
    extra=1,
    fields=('company', 'info', 'expert', 'visibility_mail',
                  'visibility_company', 'visibility_info',
                  'visibility_first_name','visibility_last_name',)
)

