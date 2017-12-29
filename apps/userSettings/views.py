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

from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
from apps.userSettings.forms import ProfileSettingsForm
from apps.user.models import User
from apps.profile.models import Profile

'''UserSettings'''
def userSettings(request):
    '''Submit Press'''
    if request.method == 'POST':

        update_data = request.POST.copy()
        try:
            userProfile = request.user.profile
        except ObjectDoesNotExist:
            userProfile = Profile(user=request.user)

        # prueft of Submit "Speichern" war
        if 'saveUser' in update_data:
            # Output Value '' fuer Checkboxen --> 0 fuer Datenbank
            if not ('expert' in update_data):
                update_data.update({'expert': 0})
            if not ('visibility_company' in update_data):
                update_data.update({'visibility_company': 0})
            if not ('visibility_info' in update_data):
                update_data.update({'visibility_info': 0})
            if not ('visibility_mail' in update_data):
                update_data.update({'visibility_mail': 0})

            # Output Value '' fuer Textfeld --> Alte wert wieder in Datenbank
            if update_data.get('info') == '':
                update_data.update({'info': userProfile.company})
            if update_data.get('company') == '':
                update_data.update({'company': userProfile.info})

        #Uebergabe und Ueberschreibung
        form = ProfileSettingsForm(data=update_data, instance=userProfile)
        if form.is_valid():
            updated_user = form.save()
            update_session_auth_hash(request, updated_user)
            return render(request, 'userSettings/index.html',
                              {'change': 'Ihre User Daten wurden erfolgreich geändert und gespeichert!'})
        else:
            return render(request, 'userSettings/index.html', {'change': 'Error Invalid form'})

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

        else:
            mes = render_to_string('userSettings/newMail.html', {
                'domain': get_current_site(request),
                'mail' : mailer.get('mail'),
                'uid': urlsafe_base64_encode(force_bytes(request.user.mail)),
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
            return HttpResponse('noch im test')
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