'''
Views of the register app.
'''
from django.shortcuts import render
from django.views.generic import FormView
from .forms import RegisterForm
from django.contrib.auth import get_user_model

#class IndexView(TemplateView):
#    User = get_user_model()
#    def get(self, request):
#        return render(request, 'register/index.html')
#    def post(self, request):
#        username = request.POST['input-password']
#        email = request.POST['input-mail']
#        user = self.User.objects.create_user(email, username)
#        user.save()
#        return render(request, 'register/index.html')


class IndexView(FormView):
    template_name = 'register/index.html'
    form_class = RegisterForm
    success_url = '/register'
    def form_valid(self, form):
            form.save()
            return super().form_valid(form)