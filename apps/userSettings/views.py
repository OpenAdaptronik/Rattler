from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect

from apps.userSettings.forms import UserSettingsForm

'''UserSettings'''
def userSettings(request):

    '''Submit Press'''
    if request.method == 'POST':
        #prueft of Submit "Speichern" war
        if 'saveUser' in request.POST:
            #weil request.POST nicht ohne Fehlermeldung ueberschrieben oder kopiert werden kann
            resp = {'visibility_mail': request.POST.get('visibilityEmail'),
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

            form = UserSettingsForm(data=resp ,instance=request.user)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
                return render(request, 'userSettings/index.html', {'change':'Ihre User Daten wurden erfolgreich geändert und gespeichert!'})
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
        mailer = {'mail': request.POST.get('newMail1'),
                  'newMail2': request.POST.get('newMail2')
                  }
        #pueft auf verschiedene fehler
        if not mailer.get('newMail2') == mailer.get('mail'):
            messages.error(request, {'error': 'Email Adresse stimmt nicht überein!'})

        else:


            # sende mail, mit Token
            return render(request,'Email wurde verschickt. Solange diese nicht bestätigt wurde beleibt die alte Email zum Login aktuell')



    return render(request, 'userSettings/changeEmail.html')
def changeEmailsucess (request,Token,mailer):

    #check Token

    # Falls token anufgerufen änder mail hiermit
        form = UserSettingsForm(data=mailer, instance=request.user)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('/settings/')
        return render(request, 'userSettings/index.html')