from django.shortcuts import render
from apps.user.models import User
from apps.profile.models import Profile


'''Community'''


def user_filter(request):
    # Submit User Search
    if request.method == 'POST':
        post_data = request.POST.copy()
        username = post_data['username']
        company = post_data['company']
        email = post_data['mail']
        # empty search
        if (username == '') and (email == '') and (company == ''):
            return render(request, 'community/index.html', {'empty_search': 'Please enter something!'})
        # legitimate search
        filtered_ids = list(User.objects.values_list('id', flat=True))
        if not(username == ''):
            matching_ids = list(User.objects.filter(username__icontains=username).values_list('id', flat=True))
            filtered_ids = list(set(matching_ids) & set(filtered_ids))
        if not(email == ''):
            matching_ids = list(User.objects.filter(mail=email).values_list('id', flat=True))
            filtered_ids = list(set(matching_ids) & set(filtered_ids))
        if not(company == ''):
            matching_ids = list(Profile.objects.filter(company=company).values_list('userID_id', flat=True))
            filtered_ids = list(set(matching_ids) & set(filtered_ids))
        i = 0
        filtered_usernames = list()
        while i < len(filtered_ids):
            currid = filtered_ids[i]
            filtered_usernames.append(User.objects.get(id=currid).username)
            i += 1
        # no id matches
        if len(filtered_ids) == 0:
            return render(request, 'community/index.html', {'no_match': 'No user matches with your search, try again!'})

        return render(request, 'community/index.html', {'filtered_usernames': filtered_usernames})

    return render(request, 'community/index.html')
