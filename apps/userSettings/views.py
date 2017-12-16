from django.shortcuts import render

# Create your views here.
from apps.userSettings.forms import UserSettings
from apps.profile.models import Profile

'''changes company and info'''


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
            form.save()
    return render(request, 'userSettings/index.html')


'''changes password'''


def ChangePassword(request):

    return render(request, 'userSettings/ChangePassword.html')
