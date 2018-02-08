from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.contrib.auth import login
from django.db import transaction

from django.shortcuts import render, reverse, redirect, HttpResponse
from django.utils.functional import lazy
from django.views.generic import UpdateView, DetailView

from django.template.loader import render_to_string
from django.contrib.auth import get_user_model

from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode

from apps.register.tokens import account_activation_token
from . import models
from . import forms
from . models import ProfileImage
from apps.user.models import User


reverse_lazy = lazy(reverse, str)

@login_required
def show_me(request):
    ''' shows user profile '''
    return render(
        request,
        'profile/me.html',
        {
            'last_projects': request.user.project_set.order_by('-updated', '-created')[:5]
        }
    )

def show(request, name = 'me'):
    if (name == 'me'):
        return show_me(request)
    user = get_user_model().objects.get(username=name)
    return render(
        request,
        'profile/profile.html',
        {
            'profile': user.profile,
            'last_projects': user.project_set.filter(visibility=True).order_by('-updated', '-created')[:5]
        }
    )

class ProfileUpdate(LoginRequiredMixin, UpdateView):
    success_url=reverse_lazy('profile:index')
    model = models.Profile
    template_name_suffix = '_update'
    fields = ['company', 'info', 'visibility_mail', 'visibility_company', 'visibility_info','visibility_first_name','visibility_last_name','expert']

    def get_object(self):
        try:
            return self.request.user.profile
        except ObjectDoesNotExist:
            return models.Profile(user=self.request.user)

    def get_context_data(self, **kwargs):
        data = super(ProfileUpdate, self).get_context_data(**kwargs)
        if self.request.method == 'POST':
            data['first_name'] = self.request.POST.get('first_name')
            data['last_name'] = self.request.POST.get('last_name')
            data['profile_image'] = forms.ProfileImageFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            data['profile_image'] = forms.ProfileImageFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        profile_image = context['profile_image']
        UserForm = forms.UserForm(data=context, instance=self.request.user)

        self.object = form.save()

        if UserForm.is_valid():
            UserForm.save()

        if profile_image.is_valid():
            profile_image.save()
        return super(ProfileUpdate, self).form_valid(form)



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


def deleteProfileImage(request):
    try:
        request.user.profile.profileimage.delete()
    except ProfileImage.DoesNotExist:
        pass
    return redirect(reverse('profile:edit'))


def change_email(request):
    if request.method == 'POST':
        mailer = {'newMail1': request.POST.get('mail'),
                  'newMail2': request.POST.get('newMail2'),}
        mail = mailer.get('newMail1')
        try:
            # prueft auf verschiedene fehler (dopplung in DB und beide felder gleich)
            if not mailer.get('newMail2') == mail:
                return render(request, 'profile/changeEmail.html',{'error': 'E-mail Adresse stimmt nicht überein!'})
            elif mail == '':
                return render(request, 'profile/changeEmail.html', {'error': 'Bitte geben sie eine Email Adresse an'})
            else:
                mailc = get_user_model().objects.get(email=mail)
                return render(request, 'profile/changeEmail.html', {'error': 'E-mail bereits vergeben'})
        except:
            mailc=None
        if mailc is None:
            token = account_activation_token.make_token(request.user)
            uid = urlsafe_base64_encode(force_bytes(request.user.pk)).decode()
            umail = urlsafe_base64_encode(force_bytes(mail)).decode()
            current_site = get_current_site(request)
            domain = current_site.domain

            mes = render_to_string('profile/newMail.html', {
                'use_https': request.is_secure(),
                'domain':domain,
                'uid': uid,
                'token': token,
                'mail': umail,
                'user': request.user,
            })

            email = EmailMessage(
                subject='Rattler: Email ändern',
                body=mes,
                to=[mail]
            )
            email.send()

            update_session_auth_hash(request, request.user)
            return HttpResponse('''Die E-mail wurde verschickt.  <br/>
                                Bitte neue E-Mail Adresse Bestätigen.<br/>
                                Solange diese nicht bestätigt wurde beleibt die alte E-mail zum Login aktuell.
                                <br/>
                                <br/>
                                Man muss beim bestätigen der E-mail weiterhin eingelogt bleiben!!''')


    return render(request, 'profile/changeEmail.html')


def change_email_success (request, mail, uidb64, token):
    # get user from user id
    from django.contrib.auth import get_user_model
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None

    if not user is None:
        email = force_text(urlsafe_base64_decode(mail))
        user.email = email
        user.save()
        update_session_auth_hash(request, user)
        login(request=request,user= user)
        return redirect(reverse('profile:edit'))
    else:
        return HttpResponse('Aktivierungslink ist ungültig oder fehler beim User!')


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect(reverse('profile:edit'))
        else:
            messages.error(request, 'Neues Passwort stimmt nicht überein')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'profile/changePassword.html', {
        'form': form
    })