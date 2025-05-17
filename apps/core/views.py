from django.http import HttpResponse
from django.shortcuts import render

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