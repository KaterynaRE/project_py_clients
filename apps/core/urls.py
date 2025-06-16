from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views.generic import RedirectView, ListView

from apps.core import views
from apps.core.views import hello, about_project, about_core

# оголосити простір імен для додатку коре
app_name = 'core'

urlpatterns = [
    # path('', hello),
    # about-core адреса має писатись в стилі кебаб-кейс
    path('about/', about_project, name='about_project'),
    path('about/core/', about_core, name='about_core'),

    path('welcome/', views.welcome, name='welcome'),
    path('treatment/', views.treatment, name='treatment'),
    path('treatment/<int:pk>/', views.TreatmentDetailUpdateView.as_view(), name='treatment_detail'),

    path('appointments/', views.appointments, name='appointments'),
    path('appointments/<int:pk>/', views.AppointmentsDetailUpdateView.as_view(), name='appointments_detail'),

    path('medical_history/', views.medical_history, name='medical_history'),
    path('medical_history/<int:pk>/', views.MedicalHistoryDetailUpdateView.as_view(), name='medical_history_detail'),

    # path('', RedirectView.as_view(pattern_name='core:clients', permanent=True)),
    path('', RedirectView.as_view(pattern_name='core:clients', permanent=False), name='home'),
    path('clients/', views.clients, name='clients'),  # core:clients
    path('clients/create/', views.create_client, name='create_client'),

    path('clients/<int:pk>/', views.ClientDetailUpdateView.as_view(), name='client_detail'),  # core:client_detail
    path('clients/<int:pk>/address-form', views.address_form, name='address_form'),
    path('clients/<int:pk>/address-delete', views.address_delete, name='address_delete'),
    path('clients/<int:pk>/phone-form', views.phone_form, name='phone_form'),

    path('doctors/', views.doctors, name='doctors'),  # core:doctors
    path('doctors/<int:pk>/', views.DoctorDetailUpdateView.as_view(), name='doctor_detail'),  # core:doctor_detail

    path('qualifications/', views.qualifications, name='qualifications'),
    path('qualifications/<int:pk>/', views.QualificationDetailUpdateView.as_view(), name='qualification_detail'),
]
