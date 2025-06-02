from sys import prefix

from django import views
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from apps.core.forms import ClientForm, AddressForm, DoctorForm, PhoneForm, QualificationForm, AppointmentForm
from apps.core.models import Client, Doctor, Qualification, Appointment
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

#security 1
def about_core(request):
    return render(request, 'core/about_core.html')

@require_http_methods(['GET'])
def clients(request):
    # Get
    context = {
        'client_list': Client.objects.all(),
        'gender_choices': Gender,
    }
    return render(request, 'core/pages/clients.html', context)

# явно обмежити типи запитів les 19.05
@require_http_methods(['GET', 'POST'])
def create_client(request):
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
        'gender_choices': Gender,
    }
    return render(request, 'core/pages/create_client.html', context)

@require_http_methods(['GET', 'POST'])
def doctors(request):
    #Post
    if request.method == 'POST':
        surname = request.POST.get('surname')
        firstname = request.POST.get('firstname')
        patronymic = request.POST.get('patronymic')
        Doctor.objects.create(
            surname = surname,
            firstname = firstname,
            patronymic = patronymic,
        )
        return redirect('core:doctors')

    # Get
    context = {
        'doctor_list': Doctor.objects.all(),
    }
    return render(request, 'core/pages/doctors.html', context)

@require_http_methods(['GET', 'POST'])
def qualifications(request):
    #Post
    if request.method == 'POST':
        form = QualificationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('core:qualifications')
    else:
        form = QualificationForm()
    # Get
    context = {
        'qualification_list': Qualification.objects.all(),
        'form': form,
    }
    return render(request, 'core/pages/qualifications.html', context)

class QualificationDetailUpdateView(views.View):
    def get(self, request, pk):
        qualification = get_object_or_404(Qualification, pk=pk)
        print(qualification)
        qualification_form = QualificationForm(instance=qualification, prefix='qualification')
        context = {
            'qualification_form' : qualification_form,
        }
        return render(request, 'core/pages/qualification_detail.html', context)

    def post(self, request, pk):
        qualification = get_object_or_404(Qualification, pk=pk)
        qualification_form = QualificationForm(request.POST, request.FILES,instance=qualification, prefix='qualification')
        if 'update_qualification' in request.POST:
            if qualification_form.is_valid():
                qualification_form.save()
                return redirect('core:qualifications')
            else:
                print(qualification_form.errors)
        elif 'submit_qualification_delete' in request.POST:
            if qualification_form.is_valid():
                qualification.delete()
                return redirect('core:qualifications')
            else:
                print(qualification.errors)
        context = {
            'qualification_form': qualification_form,
        }
        return render(request, 'core/pages/qualification_detail.html', context)


class DoctorDetailUpdateView(views.View):
    def get(self, request, pk):
        doctor = get_object_or_404(Doctor, pk=pk)
       #qualification_list = doctor.qualifications.all()
        print(doctor)
        doctor_form = DoctorForm(instance=doctor, prefix='doctor')
        #qualification_list_form = [QualificationForm(instance=qualification, prefix=str(i)) for i, qualification in enumerate(qualification_list)]
        #qualification_form = QualificationForm(prefix='qualification_name')
        context = {
            'doctor_form' : doctor_form,
            'doctor': doctor,
            # 'qualification_list_form': qualification_list_form,
            # 'qualification_form': qualification_form,
        }
        return render(request, 'core/pages/doctor_detail.html', context)

    def post(self, request, pk):
        doctor = get_object_or_404(Doctor, pk=pk)
        doctor_form = DoctorForm(request.POST, request.FILES,instance=doctor, prefix='doctor')

        if 'submit_doctor' in request.POST:
            if doctor_form.is_valid():
                doctor_form.save()
                return redirect('core:doctor_detail', pk=doctor.pk)
            else:
                print(doctor_form.errors)
        # elif 'submit_qualification' in request.POST:
        #     qualification_form = QualificationForm(request.POST, prefix='qualification_name')
        #     if qualification_form.is_valid():
        #         qualification = qualification_form.save(commit=False)
        #         qualification.doctor = doctor
        #         qualification.save()
        #         return redirect('core:doctor_detail', pk=doctor.pk)
        #     else:
        #         print(qualification_form.errors)
        # qualification_list = doctor.qualifications.all()
        # qualification_list_form = [QualificationForm(instance=qualification, prefix=str(i)) for i, qualification in enumerate(qualification_list)]
        context = {
            'doctor_form': doctor_form,
            'doctor': doctor,
            # 'qualification_list_form': qualification_list_form,
            # 'qualification_list': qualification_list,
        }
        return render(request, 'core/pages/doctor_detail.html', context)

#security LoginRequiredMixin має наслідуватись першим
class ClientDetailUpdateView(views.View):
    def get(self, request, pk):

        #спроба отримати клієнтів
        client = get_object_or_404(Client, pk=pk)
        address = getattr(client, 'address', None)
        phone_list = getattr(client, 'phones', None).all()

        print(client)
        #створення об'єкта форми, з даними client, instance заповнює форму
        client_form = ClientForm(instance=client, prefix='client') #client-surname
        address_form = AddressForm(instance=address, prefix='address')
        phone_form_list = [PhoneForm(instance=phone, prefix=str(i)) for i, phone in enumerate(phone_list)]
        phone_form = PhoneForm(prefix='phone')

        #передача форми на сторінку
        context = {
            'client_form' : client_form,
            'address_form' : address_form,
            'client': client,
            'phone_form_list': phone_form_list,
            'phone_form': phone_form
        }
        return render(request, 'core/pages/client_detail.html', context)

    def post(self, request, pk):

        client = get_object_or_404(Client, pk=pk)
        address = getattr(client, 'address', None)

        phone_form = PhoneForm(request.POST, prefix='phone')
        client_form = ClientForm(request.POST, instance=client, prefix='client')
        address_form = AddressForm(request.POST, instance=address, prefix='address')

        if 'submit_client' in request.POST:
            if client_form.is_valid():
                client_form.save()
                return redirect('core:client_detail', pk=client.pk)
            else:
                print(client_form.errors)
        elif 'submit_delete_client' in request.POST:
            if client:
                client.delete()
                return redirect('core:clients')
            else:
                print(client.errors)

        elif 'submit_address' in request.POST:
            if address_form.is_valid():
                address = address_form.save()
                client.address = address
                client.save()
                return redirect('core:client_detail', pk=client.pk)
            else:
                print(address_form.errors)
        elif 'address_delete_btn' in request.POST:
            address = getattr(client, 'address', None)
            print(f"Address before deletion: {address}")
            if address:
                address.delete()
                client.address = None
                client.save()
                print("Address deleted")
                return redirect('core:client_detail', pk=client.pk)

        elif 'submit_phone_add' in request.POST:
            if phone_form.is_valid():
                phone = phone_form.save()
                phone.client = client
                phone.save()
                return redirect('core:client_detail', pk=client.pk)
            else:
                print(phone_form.errors)
        elif 'submit_phone_update' in request.POST:
            try:
                index = int(request.POST.get('submit_phone_update'))
                phone = client.phones.all()[index]
                phone_form = PhoneForm(request.POST, instance=phone, prefix=str(index))
                if phone_form.is_valid():
                    phone_form.save()
                    return redirect('core:client_detail', pk=client.pk)
                else:
                    print(phone_form.errors)
            except (IndexError, ValueError):
                pass
        elif 'submit_phone_delete' in request.POST:
            prefix = request.POST.get('submit_phone_delete')
            phone_list = client.phones.all()
            try:
                phone = phone_list[int(prefix)]
            except (IndexError | ValueError):
                return redirect('core:client_detail', pk=client.pk)
            phone.delete()
            return redirect('core:client_detail', pk=client.pk)

        phone_list = client.phones.all()
        phone_form_list = [PhoneForm(instance=phone, prefix=str(i)) for i, phone in enumerate(phone_list)]

        #Рендер у випадку помилки, залишаємо данні введені у формі
        context = {
            'client_form': client_form,
            'address_form': address_form,
            'client': client,
            'phone_form': phone_form,
            'phone_form_list': phone_form_list,
        }
        return render(request, 'core/pages/client_detail.html', context)

# path('clients/<int:pk>/address-form'
def address_form(request, pk):
    print('views address_form')
    print(request)
    if request.method == 'POST':
        #city = request.POST.get('city')
        client = get_object_or_404(Client, pk=pk)
        address = getattr(client, 'address', None)
        address_form = AddressForm(request.POST, instance=address, prefix='address')

        if address_form.is_valid():
            address = address_form.save()
            client.address = address
            client.save()
            return JsonResponse({'success': True, 'message': f'Successfully updated address for Client {pk}'})
        else:
            return JsonResponse({
                'success': False,
                'message': 'Form is not valid',
                'errors': address_form.errors,
            }, status=400)
    return JsonResponse({'message': f'Wrong method'}, status=400)

@require_http_methods(["POST", "GET"])
def address_delete(request, pk):
    client = get_object_or_404(Client, pk=pk)
    address = getattr(client, 'address', None)

    if address:
        address.delete()
        client.address = None
        client.save()
        return JsonResponse({'success': True, 'message': f'Address deleted for client {pk}'})
    return JsonResponse({'success': False, 'message': 'No address to delete'}, status=400)


def phone_form(request, pk):
    print('views phone_form')
    print(request)
    if request.method == 'POST':
        client = get_object_or_404(Client, pk=pk)
        phone_form = PhoneForm(request.POST, prefix='phone')
        if phone_form.is_valid():
            phone = phone_form.save()
            phone.client = client
            phone.save()
            client.save()
            return JsonResponse({'success': True,'message': f'Successfully updated phone for Client {pk}'})
    return JsonResponse({'message': f'Wrong method'}, status=400)


def welcome(request):
    return render(request, 'core/pages/welcome.html')


@require_http_methods(['GET', 'POST'])
def appointments(request):
    #Post
    if request.method == 'POST':
        day_to_appointment = request.POST.get('day_to_appointment')
        reason_for_request = request.POST.get('reason_for_request')
        Appointment.objects.create(
            day_to_appointment = day_to_appointment,
            reason_for_request = reason_for_request,
        )
        return redirect('core:appointments')

    # Get
    context = {
        'appointment_list': Appointment.objects.all(),
    }
    return render(request, 'core/pages/appointments.html', context)
