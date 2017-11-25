from django.shortcuts import render

def index(request):
    context = {
        'test': 'Hallo Welt. Next',
        'value': None
    }

    if request.method == 'POST':
        context.update({'value': request.POST['value']})
    return render(request, 'index/index.html', context)


