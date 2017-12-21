from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render


'''Community'''
def projectFilter(request):
    '''Submit Press'''
    if request.method == 'POST':

        post_data = request.POST.copy()

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
            updated_user = form.save()
            update_session_auth_hash(request, updated_user)
            return render(request, 'community/index.html',
                              {'change': 'Ihre User Daten wurden erfolgreich geändert und gespeichert!'})
        else:
            return render(request, 'community/index.html', {'change': 'Error Invalid form'})

    return render(request, 'community/index.html')
