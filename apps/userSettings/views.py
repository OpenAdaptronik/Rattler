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
from apps.userSettings.forms import UserSettingsForm

'''UserSettings'''
def userSettings(request):

    '''Submit Press'''
    if request.method == 'POST':
        #prueft of Submit "Speichern" war
        if 'saveUser' in request.POST:
            #weil request.POST nicht ohne Fehlermeldung ueberschrieben oder kopiert werden kann
            resp = {'mail': request.user.mail,
                    'visibility_mail': request.POST.get('visibilityEmail'),
                    'company': request.POST.get('company'),
                    'visibility_company': request.POST.get('visibilityCompany'),
                    'info' : request.POST.get('info'),
                    'visibility_info':request.POST.get('visibilityInfo')
                    }
            #checkboxen IM html dokument haben ihre Probleme
            # Output Value '' --> 0 fuer Datenbank
            if resp.get('visibility_mail') == '':
                resp.update({'visibility_mail': '0'})

            # Output Value '' --> 0 fuer Datenbank
            if resp.get('visibility_company') == '':
                resp.update({'visibility_company': '0'})

            # Output Value '' --> 0 fuer Datenbank
            if resp.get('visibility_info') == '':
                resp.update({'visibility_info': '0'})

            #prueft auf leere feld "Firma"
            if resp.get('company') == '':
                resp.update({'company': request.user.company})

            #prueft auf leere feld "info"
            if resp.get('info') == '':
                resp.update({'info': request.user.info})

            form = UserSettingsForm(data=resp,instance=request.user)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
                return render(request, 'userSettings/index.html',{'change':'Ihre User Daten wurden erfolgreich geändert und gespeichert!'})
            else:
                return render(request, 'userSettings/index.html',{'change': 'Error Invalid form'})
        #Experten Settings
        elif 'saveExpert' in request.POST:
            return render(request, 'userSettings/index.html')

        return render(request, 'userSettings/index.html')
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
                'uid':urlsafe_base64_encode(force_bytes(request.user.pk)),
                'token':default_token_generator.make_token(request.user)
            })
            email = EmailMessage (
                    'Rattler: Email ändern',mes,'rattler@openadaptronik.com',mailer.get('mail'))
            email.send()
            return HttpResponse('''Bitte neue E-Mail Adresse Bestätigen. <br/>
                                Die E-mail wurde verschickt. <br/>
                                Solange diese nicht bestätigt wurde beleibt die alte E-mail zum Login aktuell.''')

    return render(request, 'userSettings/changeEmail.html')
def changeEmailsucess (request,email,uidb64,token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = request.user.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, request.user.DoesNotExist):
            user = None
        if user is not None and default_token_generator.check_token(user, token):
            user.mail = email
            user.save()
            login(request, user)
            # return redirect('home')
            return HttpResponse('Neue E-Mail wurde bestätigt')
        else:
            return HttpResponse('Aktivierungslink ist ungültig!')