from django import views
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods

from apps.core.forms import ClientForm
from apps.core.models import Client
from apps.core.models.client import Gender


# Create your views here.
#приймає об'єкт запиту від браузера
def hello(request):
    #return HttpResponse("Hello")
    #mime type
    #return HttpResponse("Hello", content_type='text/plain')
    return HttpResponse("<h1>Hello W</h1>", content_type='text/html')

def about_project(request):
    return render(request, 'about_project.html')

def about_core(request):
    return render(request, 'core/about_core.html')


# явно обмежити типи запитів les 19.05
@require_http_methods(['GET', 'POST'])
def clients(request):
    #Post
    if request.method == 'POST':
        surname = request.POST.get('surname')
        firstname = request.POST.get('firstname')
        patronymic = request.POST.get('patronymic')
        birthday = request.POST.get('birthday')
        email = request.POST.get('email')
        gender = request.POST.get('gender')

        #можна додати валідацію на рівні сервера
        Client.objects.create(
            surname = surname,
            firstname = firstname,
            patronymic = patronymic,
            birthday = birthday,
            email = email,
            gender = gender
        )
        return redirect('core:clients')

    # Get
    context = {
        'client_list': Client.objects.all(),
        'gender_choices': Gender,
    }
    return render(request, 'core/pages/clients.html', context)

class ClientDetailUpdateView(views.View):
    def get(self, request, pk):
        client = get_object_or_404(Client, pk=pk)
        print(client)
        client_form = ClientForm(instance=client)

        context = {
            'client_form' : client_form,

        }
        return render(request, 'core/pages/client_detail.html', context)

    def post(self, request, pk):
        pass