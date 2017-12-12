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
            resp = {'visibility_mail': request.POST.get('visibility_mail'),
                    'company': request.POST.get('company'),
                    'visibility_company': request.POST.get('visibility_company'),
                    'info' : request.POST.get('info'),
                    'visibility_info':request.POST.get('visibility_info')
                    }
            ''' checkboxen IM html dokument haben ihre Probleme
            # Output Value '' --> 0 für Datenbank
            if resp.get('visibility_mail') == '':
                resp.update({'visibility_mail': '0'})
            if resp.get('visibility_mail') == 'on':
                resp.update({'visibility_company': '1'})'''
            #prueft auf leere feld "Firma"
            if resp.get('company') == '':
                resp.update({'company' : request.user.company})
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
 #noch in arbeit
        return render(request, 'userSettings/changeEmail.html')