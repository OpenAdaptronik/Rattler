from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage

from django.shortcuts import render, reverse, redirect, HttpResponse
from django.utils.functional import lazy
from django.views.generic import UpdateView, DetailView


from apps.register.models import VerificationToken
from django.template.loader import render_to_string
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


def change_email(request):

    if request.method == 'POST':
        mailer = {'newMail1': request.POST.get('mail'),
                  'newMail2': request.POST.get('newMail2'),}
        mail = mailer.get('newMail1')
        try:
            # prueft auf verschiedene fehler (dopplung in DB und beide felder gleich)
            if not mailer.get('newMail2') == mail:
                return render(request, 'userSettings/changeEmail.html',{'error': 'E-mail Adresse stimmt nicht überein!'})
            elif mail == '':
                return render(request, 'userSettings/changeEmail.html', {'error': 'Bitte geben sie eine Email Adresse an'})
            else:
                mailc = User.objects.get(mail=mail)
                return render(request, 'userSettings/changeEmail.html', {'error': 'E-mail bereits vergeben'})
        except:
            mailc=None
        if mailc is None:
            try:
                token = VerificationToken.objects.create_user_token(request.user)
                mes = render_to_string('userSettings/newMail.html', {
                    'domain': get_current_site(request),
                    'mail': mail,
                    'username': request.user.username,
                    'token': token
                })

                email = EmailMessage(
                    subject='Rattler: Email ändern',
                    body=mes,
                    to=[mail]
                )
                email.send()
            except (VerificationToken.MultipleObjectsReturned):
                token = None

            update_session_auth_hash(request, request.user)
            return HttpResponse('''Die E-mail wurde verschickt.  <br/>
                                Bitte neue E-Mail Adresse Bestätigen.<br/>
                                Solange diese nicht bestätigt wurde beleibt die alte E-mail zum Login aktuell.
                                <br/>
                                <br/>
                                Sie müssen beim bestätigen der E-mail weiterhin eingelogt bleiben!!''')


    return render(request, 'userSettings/changeEmail.html')


def change_email_success (request,email,username,token):

        #checkt ob user der Eingeloggt ist auch user der mail ist
        #und ob die mail noch nicht vergeben wurde werend des Zeitfensteres des vergebens
        try:
            if request.user.username == username:
                user = User.objects.get(username=username)
                token = VerificationToken.objects.get_token(token)

        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and token.user_id == user.id:
            user.mail = email
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
    return render(request, 'userSettings/changePassword.html', {
        'form': form
    })