from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.contrib.auth import login
from apps.user.models import User

# Create your views here.
from apps.userSettings.forms import UserSettings
from apps.profile.models import Profile

'''changes company and info'''

'''UserSettings'''
def userSettings(request):
    userid = request.user.id
    current_company = Profile.objects.filter(userID=userid).values('company')
    current_info = Profile.objects.filter(userID=userid).values('info')
    if request.method == 'POST':
        form = UserSettings(data=request.POST, instance=request.user.profile)
        if form.is_valid():
            updated_data = request.POST.copy()
            if form.cleaned_data['company'] is None:
                updated_data['company'] = current_company
            if form.cleaned_data['info'] is None:
                updated_data['info'] = current_info
            if not('expert' in updated_data):
                updated_data.update({'expert': 0})
            if not('visibility_mail' in updated_data):
                updated_data.update({'visibility_mail': 0})
            if not('visibility_company' in updated_data):
                updated_data.update({'visibility_company': 0})
            if not('visibility_info' in updated_data):
                updated_data.update({'visibility_info': 0})
            form = UserSettings(data=updated_data, instance=request.user.profile)
            user = form.save()
            update_session_auth_hash(request, user)
    return render(request, 'userSettings/index.html')

'''Passwort aendern'''
def changePassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('/settings/')
        else:
            messages.error(request, 'Neues Passwort stimmt nicht überein')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'userSettings/changePassword.html', {
        'form': form
    })
'''Email aendern'''
def changeEmail(request):
    if request.method == 'POST':
        mailer = {'mail': request.POST.get('mail'),
                  'newMail2': request.POST.get('newMail2'),}
        #pueft auf verschiedene fehler
        if not mailer.get('newMail2') == mailer.get('mail'):
            return render(request, 'userSettings/changeEmail.html', {'error': 'E-mail Adresse stimmt nicht überein!'})
        # pueft auf verdopplungen
            #geht net!!!
        #if UserSettingsForm.get_initial_for_field('mail', mailer.get('mail')):
         #   messages.error(request, {'error': 'E-mail Adresse läuft bereits auf anderen User!'})

        else:
            mes = render_to_string('userSettings/newMail.html', {
                'domain': get_current_site(request),
                'mail' : mailer.get('mail'),
                'uid': urlsafe_base64_encode(force_bytes(request.user.id)),
                'token': default_token_generator.make_token(user=request.user)
            })
            email = EmailMessage(
                    subject='Rattler: Email ändern',
                    body=mes,
                    to= [mailer.get('mail')]
            )
            email.send()
            update_session_auth_hash(request, request.user)
            return HttpResponse('''Bitte neue E-Mail Adresse Bestätigen. <br/>
                                Die E-mail wurde verschickt. <br/>
                                Solange diese nicht bestätigt wurde beleibt die alte E-mail zum Login aktuell.''')

    return render(request, 'userSettings/changeEmail.html')


def changeEmailsuccess (request,email,uidb64,token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()

            return HttpResponse(uid)
            return HttpResponse('bla bla!')
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
            return HttpResponse('da da!')
        if user is not None and default_token_generator.check_token(user=request.user, token=token):
            user.mail = email
            user.save()
            login(request=request,user= user)
            # return redirect('home')
            return render(request, 'userSettings/index.html', {'change': 'E-Mail Adresse erfolgreich geändert!'})
        else:
            return HttpResponse('Aktivierungslink ist ungültig!')