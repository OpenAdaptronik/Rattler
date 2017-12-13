from django.shortcuts import render

# Create your views here.
from apps.userSettings.forms import UserSettingsForm

'''changes company and info'''

def userSettings(request):
    # respo = {'username': request.user.username, 'email': request.user.mail,
    # 'company': request.user.company, 'infos': request.user.info}
    data1 = request.user.company
    data2 = request.user.info
    if request.method == 'POST':
        form = UserSettingsForm(data=request.POST, instance=request.user)
        if form.is_valid():
            updated_data = request.POST.copy()
            if form.cleaned_data['company'] is None:
                updated_data['company'] = data1
            if form.cleaned_data['info'] is None:
                updated_data['info'] = data2
            form = UserSettingsForm(data=updated_data, instance=request.user)
            form.save()
    return render(request, 'userSettings/index.html')


'''changes password'''
def ChangePassword(request):

    return render(request, 'userSettings/ChangePassword.html')
