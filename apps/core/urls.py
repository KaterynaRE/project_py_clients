from django.urls import path

from apps.core.views import hello, about_project, about_core

urlpatterns = [
    #path('', hello),
    path('', about_project),
    path('core/', about_core),
    # about-core адреса має писатись в стилі кебаб-кейс
    path('about-core/', about_core),
    path('about/', about_project),
    path('about/core/', about_core),
]