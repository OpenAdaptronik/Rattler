from django.shortcuts import render, reverse
from django.utils.functional import lazy
from django.views.generic import UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth import get_user_model

# curent user model


from . import models

reverse_lazy = lazy(reverse, str)

@login_required
def show_me(request):
    ''' shows user profile '''
    return render(request, 'profile/me.html')

def show(request, name = 'me'):
    if (name == 'me'):
        return show_me(request)
    user = get_user_model().objects.get(username=name)
    return render(request, 'profile/profile.html', {'user':user})

class ProfileUpdate(LoginRequiredMixin, UpdateView):
    success_url=reverse_lazy('profile:index')
    model = models.Profile
    template_name_suffix = '_update'
    fields = ['company', 'info', 'visibility_mail', 'visibility_company', 'visibility_info']

    def get_object(self):
        try:
            return self.request.user.profile
        except ObjectDoesNotExist:
            return models.Profile(user=self.request.user)

class ProfileImageUpdate(LoginRequiredMixin, UpdateView):
    success_url=reverse_lazy('profile:index')
    model = models.ProfileImage
    template_name_suffix = '_update'
    fields = ['path']

    def get_object(self):
        profile = ProfileUpdate(request=self.request).get_object()
        try:
            return profile.profileimage
        except ObjectDoesNotExist:
            return models.ProfileImage(profile=profile)
