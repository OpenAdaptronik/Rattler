from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.contrib.auth import login
from apps.register.models import VerificationToken



# Create your views here.
from apps.userSettings.forms import ProfileSettingsForm
from apps.user.models import User


'''UserSettings'''
def userSettings(request):
    '''Submit Press'''
    if request.method == 'POST':

        update_data = request.POST.copy()
        userProfile = request.user.profile

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


def changeEmailsuccess (request,email,username,token):

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
            # return redirect('settings')
            return redirect('/settings/')
        else:
            return HttpResponse('Aktivierungslink ist ungültig oder fehler beim User!')
