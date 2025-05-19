from django.urls import path
from django.views.generic import RedirectView, ListView

from apps.core import views
from apps.core.views import hello, about_project, about_core
#оголосити простір імен для додатку коре
app_name = 'core'

urlpatterns = [
    #path('', hello),
    # about-core адреса має писатись в стилі кебаб-кейс
    path('about/', about_project),
    path('about/core/', about_core),

    path('',RedirectView.as_view(pattern_name='core:clients', permanent=True)),
    path('clients/', views.clients, name='clients'), # core:clients
]