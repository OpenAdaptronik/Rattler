from django.shortcuts import render
from apps.user.models import User
from apps.profile.models import Profile
from apps.projects.models import Project


'''Community'''


def user_filter(request):
    # Submit User Search
    if request.method == 'POST':
        post_data = request.POST.copy()
        username = post_data['username']
        company = post_data['company']
        email = post_data['mail']
        project_name = post_data['projectname']
        category = post_data['category']
        manufacturer = post_data['manufacturer']
        # empty search
        if (username == '') and (email == '') and (company == '') and (project_name == '') and (category == '') and (manufacturer == ''):
            return render(request, 'community/index.html', {'empty_search': 'Bitte gib einen Suchbegriff ein!'})
        # legitimate search
        filtered_ids = list(Project.objects.values_list('id', flat=True))
        if not(username == ''):
            matching_ids = list(Project.objects.filter(user__username__icontains=username).values_list('id', flat=True))
            filtered_ids = list(set(matching_ids) & set(filtered_ids))
        if not(email == ''):
            matching_ids = list(Project.objects.filter(user__email__icontains=email).values_list('id', flat=True))
            filtered_ids = list(set(matching_ids) & set(filtered_ids))
        if not(company == ''):
            matching_ids = list(Project.objects.filter(user__profile__company__icontains=company).values_list('id', flat=True))
            filtered_ids = list(set(matching_ids) & set(filtered_ids))
        if not(project_name == ''):
            matching_ids = list(Project.objects.filter(name__icontains=project_name).values_list('id', flat=True))
            filtered_ids = list(set(matching_ids) & set(filtered_ids))
        if not(category == ''):
            matching_ids = list(Project.objects.filter(category__name__icontains=category).values_list('id', flat=True))
            filtered_ids = list(set(matching_ids) & set(filtered_ids))
        if not(manufacturer == ''):
            matching_ids = list(Project.objects.filter(manufacturer__icontains=manufacturer).values_list('id', flat=True))
            filtered_ids = list(set(matching_ids) & set(filtered_ids))
        #return usernames in filtered_usernames
        i = 0
        filtered_projects = list()
        while i < len(filtered_ids):
            currid = filtered_ids[i]
            filtered_projects.append(Project.objects.get(id=currid))
            i += 1

        j = 0
        filtered_users = list()
        while j < len(filtered_ids):
            currprojectid = filtered_ids[j]
            curruserid = Project.objects.get(id = currprojectid).user_id
            filtered_users.append(User.objects.get(id=curruserid))
            j += 1

        filtered = zip(filtered_users, filtered_projects)



        # no id matches
        if len(filtered_ids) == 0:
            return render(request, 'community/index.html', {'no_match': 'No user matches with your search, try again!'})

        return render(request, 'community/index.html', {'filtered_ids': filtered_ids, 'filtered_projects': filtered_projects, 'filtered': filtered})

    return render(request, 'community/index.html')
