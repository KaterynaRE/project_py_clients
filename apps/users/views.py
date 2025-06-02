from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic, View

from apps.users.forms import CustomUserCreationForm
from apps.users.models import CustomUser


# Create your views here.
class RegisterView(generic.CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'
    #success_url = reverse_lazy('login')
    success_url = reverse_lazy('core:welcome')

@method_decorator(login_required, name='dispatch')
class UserListView(View):
    template_name = 'registration/users.html'

    def get(self, request):
        users = CustomUser.objects.all()
        return render(request, self.template_name, {'users': users})

    def post(self, request):
        for key, value in request.POST.items():
            if key.startswith('role_'):
                user_id = key.split('_')[1]
                try:
                    user = CustomUser.objects.get(id=user_id)
                    user.role = value
                    user.save()
                except CustomUser.DoesNotExist:
                    pass
        return redirect('users')