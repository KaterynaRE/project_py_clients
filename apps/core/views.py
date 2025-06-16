from datetime import datetime
from sys import prefix

from django import views
from django.contrib.auth.decorators import login_required
from django.db.models.functions import NullIf
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from apps.core.forms import ClientForm, AddressForm, DoctorForm, PhoneForm, QualificationForm, AppointmentForm, \
    AddQualificationForm, AddClientForm, AddDoctorForm, MedicalHistoryForm, TreatmentForm
from apps.core.models import Client, Doctor, Qualification, Appointment, MedicalHistory, Treatment
from apps.core.models.client import Gender


# Create your views here.
# приймає об'єкт запиту від браузера
def hello(request):
    # return HttpResponse("Hello")
    # mime type
    # return HttpResponse("Hello", content_type='text/plain')
    return HttpResponse("<h1>Hello W</h1>", content_type='text/html')


def about_project(request):
    return render(request, 'about_project.html')


# security 1
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
    # Post
    if request.method == 'POST':
        surname = request.POST.get('surname')
        firstname = request.POST.get('firstname')
        patronymic = request.POST.get('patronymic')
        birthday = request.POST.get('birthday')
        email = request.POST.get('email')
        gender = request.POST.get('gender')

        # можна додати валідацію на рівні сервера
        Client.objects.create(
            surname=surname,
            firstname=firstname,
            patronymic=patronymic,
            birthday=birthday,
            email=email,
            gender=gender
        )
        return redirect('core:clients')

    # Get
    context = {
        'gender_choices': Gender,
    }
    return render(request, 'core/pages/create_client.html', context)


@require_http_methods(['GET', 'POST'])
def doctors(request):
    # Post
    if request.method == 'POST':
        surname = request.POST.get('surname')
        firstname = request.POST.get('firstname')
        patronymic = request.POST.get('patronymic')
        Doctor.objects.create(
            surname=surname,
            firstname=firstname,
            patronymic=patronymic,
        )
        return redirect('core:doctors')

    # Get
    context = {
        'doctor_list': Doctor.objects.all(),
    }
    return render(request, 'core/pages/doctors.html', context)


@require_http_methods(['GET', 'POST'])
def qualifications(request):
    # Post
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
            'qualification_form': qualification_form,
        }
        return render(request, 'core/pages/qualification_detail.html', context)

    def post(self, request, pk):
        qualification = get_object_or_404(Qualification, pk=pk)
        qualification_form = QualificationForm(request.POST, request.FILES, instance=qualification,
                                               prefix='qualification')
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
        print(doctor)
        doctor_form = DoctorForm(instance=doctor, prefix='doctor')
        qualification_list_form = [QualificationForm(instance=qualification, prefix=str(i)) for i, qualification in
                                   enumerate(doctor.qualifications.all())]
        add_qualification_form = AddQualificationForm()
        context = {
            'doctor_form': doctor_form,
            'doctor': doctor,
            'add_qualification_form': add_qualification_form,
            'qualification_list_form': qualification_list_form,
        }
        return render(request, 'core/pages/doctor_detail.html', context)

    def post(self, request, pk):
        doctor = get_object_or_404(Doctor, pk=pk)
        doctor_form = DoctorForm(request.POST, request.FILES, instance=doctor, prefix='doctor')
        add_qualification_form = AddQualificationForm(request.POST)

        if 'submit_doctor' in request.POST:
            if doctor_form.is_valid():
                doctor_form.save()
                return redirect('core:doctor_detail', pk=doctor.pk)
            else:
                print(doctor_form.errors)
        elif 'delete_doctor' in request.POST:
            if doctor_form.is_valid():
                doctor.delete()
                return redirect('core:doctors')
            else:
                print(doctor_form.errors)

        elif 'submit_qualification' in request.POST:
            if add_qualification_form.is_valid():
                qualification = add_qualification_form.cleaned_data['qualification']
                qualification.doctor = doctor
                qualification.save()
                return redirect('core:doctor_detail', pk=doctor.pk)
            else:
                print(add_qualification_form.errors)
        elif 'submit_delete_qualification' in request.POST:
            qualification_id = request.POST.get('qualification_id')
            qualification = get_object_or_404(Qualification, pk=qualification_id)
            doctor.qualifications.remove(qualification)
            return redirect('core:doctor_detail', pk=doctor.pk)

        qualification_list_form = [QualificationForm(instance=q, prefix=str(i)) for i, q in
                                   enumerate(doctor.qualifications.all())]
        context = {
            'doctor_form': doctor_form,
            'doctor': doctor,
            'add_qualification_form': add_qualification_form,
            'qualification_list_form': qualification_list_form,
        }
        return render(request, 'core/pages/doctor_detail.html', context)


# security LoginRequiredMixin має наслідуватись першим
class ClientDetailUpdateView(views.View):
    def get(self, request, pk):

        # спроба отримати клієнтів
        client = get_object_or_404(Client, pk=pk)
        address = getattr(client, 'address', None)
        doctors = client.doctors.all()
        medical_history = MedicalHistory.objects.filter(client=client).first()
        phone_list = getattr(client, 'phones', None).all()

        print(client)
        # створення об'єкта форми, з даними client, instance заповнює форму
        client_form = ClientForm(instance=client, prefix='client')  # client-surname
        add_doctor_form = AddDoctorForm(prefix='doctor')
        address_form = AddressForm(instance=address, prefix='address')
        medical_history_form = MedicalHistoryForm(instance=medical_history, prefix='medical_history')
        phone_form_list = [PhoneForm(instance=phone, prefix=str(i)) for i, phone in enumerate(phone_list)]
        phone_form = PhoneForm(prefix='phone')

        # передача форми на сторінку
        context = {
            'client_form': client_form,
            'address_form': address_form,
            'client': client,
            'phone_form_list': phone_form_list,
            'phone_form': phone_form,
            'medical_history_form': medical_history_form,
            'medical_history': medical_history,
            'doctors': doctors,
            'add_doctor_form': add_doctor_form,
        }
        return render(request, 'core/pages/client_detail.html', context)

    def post(self, request, pk):

        client = get_object_or_404(Client, pk=pk)
        address = getattr(client, 'address', None)
        medical_history = MedicalHistory.objects.filter(client=client).first()
        doctors = client.doctors.all()
        add_doctor_form = AddDoctorForm(request.POST, prefix='doctor')
        phone_form = PhoneForm(request.POST, prefix='phone')
        client_form = ClientForm(request.POST, instance=client, prefix='client')
        address_form = AddressForm(request.POST, instance=address, prefix='address')
        medical_history_form = MedicalHistoryForm(request.POST, instance=medical_history, prefix='medical_history')

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

        elif 'submit_medical_history' in request.POST:
            if medical_history_form.is_valid():
                medical_history = medical_history_form.save()
                medical_history.client = client
                medical_history.save()
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

        elif 'medical_history_delete_btn' in request.POST:
            if medical_history:
                medical_history.delete()
                return redirect('core:client_detail', pk=client.pk)

        elif 'delete_doctor' in request.POST:
            doctor_id = request.POST.get('delete_doctor')
            if doctor_id:
                try:
                    doctor = Doctor.objects.get(pk=doctor_id)
                    client.doctors.remove(doctor)
                    client.save()
                except:
                    pass
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
        elif 'add_doctor' in request.POST:
            if add_doctor_form.is_valid():
                select_doctor = add_doctor_form.cleaned_data['doctor']
                client.doctors.add(select_doctor)
                client.save()
                return redirect('core:client_detail', pk=client.pk)
            else:
                print(add_doctor_form.errors)

        phone_list = client.phones.all()
        phone_form_list = [PhoneForm(instance=phone, prefix=str(i)) for i, phone in enumerate(phone_list)]

        # Рендер у випадку помилки, залишаємо данні введені у формі
        context = {
            'client_form': client_form,
            'address_form': address_form,
            'client': client,
            'phone_form': phone_form,
            'phone_form_list': phone_form_list,
            'medical_history_form': medical_history_form,
            'add_doctor_form': add_doctor_form,
            'doctors': doctors,
        }
        return render(request, 'core/pages/client_detail.html', context)


# path('clients/<int:pk>/address-form'
def address_form(request, pk):
    print('views address_form')
    print(request)
    if request.method == 'POST':
        # city = request.POST.get('city')
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
            return JsonResponse({'success': True, 'message': f'Successfully updated phone for Client {pk}'})
    return JsonResponse({'message': f'Wrong method'}, status=400)


def welcome(request):
    return render(request, 'core/pages/welcome.html')


@require_http_methods(['GET', 'POST'])
def appointments(request):
    # Post
    if request.method == 'POST':
        day_to_appointment = request.POST.get('day_to_appointment')
        reason_for_request = request.POST.get('reason_for_request')
        Appointment.objects.create(
            day_to_appointment=day_to_appointment,
            reason_for_request=reason_for_request,
        )
        return redirect('core:appointments')

    # Get
    context = {
        'appointment_list': Appointment.objects.all(),
    }
    return render(request, 'core/pages/appointments.html', context)


class AppointmentsDetailUpdateView(views.View):
    def get(self, request, pk):
        appointment = get_object_or_404(Appointment, pk=pk)
        appointment_form = AppointmentForm(instance=appointment, prefix='appointment')

        add_client_form = AddClientForm(prefix='client')
        add_doctor_form = AddDoctorForm(prefix='doctor')

        client = appointment.client
        doctor = appointment.doctor

        context = {
            'appointment': appointment,
            'appointment_form': appointment_form,
            'add_client_form': add_client_form,
            'client': client,
            'add_doctor_form': add_doctor_form,
            'doctor': doctor,
        }
        return render(request, 'core/pages/appointments_detail.html', context)

    def post(self, request, pk):
        appointment = get_object_or_404(Appointment, pk=pk)
        appointment_form = AppointmentForm(request.POST, instance=appointment, prefix='appointment')

        add_client_form = AddClientForm(request.POST, prefix='client')
        add_doctor_form = AddDoctorForm(request.POST, prefix='doctor')

        client = appointment.client
        doctor = appointment.doctor

        if 'update_appointment' in request.POST:
            if appointment_form.is_valid():
                appointment_form.save()
                return redirect('core:appointments_detail', pk=appointment.pk)
            else:
                print(appointment_form.errors)
        elif 'delete_appointment' in request.POST:
            appointment.delete()
            return redirect('core:appointments')
        elif 'add_client' in request.POST:
            if add_client_form.is_valid():
                select_client = add_client_form.cleaned_data['client']
                appointment.client = select_client
                appointment.save()
                return redirect('core:appointments_detail', pk=appointment.pk)
            else:
                print(appointment_form.errors)
        elif 'add_doctor' in request.POST:
            if add_doctor_form.is_valid():
                select_doctor = add_doctor_form.cleaned_data['doctor']
                appointment.doctor = select_doctor
                appointment.save()
                return redirect('core:appointments_detail', pk=appointment.pk)
            else:
                print(appointment_form.errors)
        context = {
            'appointment_form': appointment_form,
            'appointment': appointment,
            'add_client_form': add_client_form,
            'client': client,
            'add_doctor_form': add_doctor_form,
            'doctor': doctor,
        }
        return render(request, 'core/pages/appointments_detail.html', context)


@require_http_methods(['GET', 'POST'])
def medical_history(request):
    # Post
    if request.method == 'POST':
        name_of_disease = request.POST.get('name_of_disease')
        diagnostic_date = request.POST.get('diagnostic_date')
        is_chronic = bool(request.POST.get('is_chronic'))
        MedicalHistory.objects.create(
            name_of_disease=name_of_disease,
            diagnostic_date=diagnostic_date,
            is_chronic=is_chronic,
        )
        return redirect('core:medical_history')

    # Get
    context = {
        'medical_history_list': MedicalHistory.objects.all(),
    }
    return render(request, 'core/pages/medical_history.html', context)


class MedicalHistoryDetailUpdateView(views.View):
    def get(self, request, pk):
        medical_history = get_object_or_404(MedicalHistory, pk=pk)
        medical_history_form = MedicalHistoryForm(instance=medical_history, prefix='medical_history')

        add_client_form = AddClientForm(prefix='client')
        add_doctor_form = AddDoctorForm(prefix='doctor')

        client = medical_history.client
        doctor = medical_history.doctor
        context = {
            'medical_history': medical_history,
            'medical_history_form': medical_history_form,
            'add_client_form': add_client_form,
            'client': client,
            'add_doctor_form': add_doctor_form,
            'doctor': doctor,
        }
        return render(request, 'core/pages/medical_history_detail.html', context)

    def post(self, request, pk):
        medical_history = get_object_or_404(MedicalHistory, pk=pk)
        medical_history_form = MedicalHistoryForm(request.POST, instance=medical_history, prefix='medical_history')

        add_client_form = AddClientForm(request.POST, prefix='client')
        add_doctor_form = AddDoctorForm(request.POST, prefix='doctor')

        client = medical_history.client
        doctor = medical_history.doctor
        if 'update_medical_history' in request.POST:
            if medical_history_form.is_valid():
                medical_history_form.save()
                return redirect('core:medical_history_detail', pk=medical_history.pk)
            else:
                print(medical_history_form.errors)
        elif 'delete_medical_history' in request.POST:
            medical_history.delete()
            return redirect('core:medical_history')

        elif 'add_client' in request.POST:
            if add_client_form.is_valid():
                select_client = add_client_form.cleaned_data['client']
                medical_history.client = select_client
                medical_history.save()
                return redirect('core:medical_history_detail', pk=medical_history.pk)
            else:
                print(add_client_form.errors)
        elif 'delete_client' in request.POST:
            medical_history.client = None
            medical_history.save()
            return redirect('core:medical_history_detail', pk=medical_history.pk)
        elif 'delete_doctor' in request.POST:
            medical_history.doctor = None
            medical_history.save()
            return redirect('core:medical_history_detail', pk=medical_history.pk)

        elif 'add_doctor' in request.POST:
            if add_doctor_form.is_valid():
                select_doctor = add_doctor_form.cleaned_data['doctor']
                medical_history.doctor = select_doctor
                medical_history.save()
                return redirect('core:medical_history_detail', pk=medical_history.pk)
            else:
                print(add_doctor_form.errors)
        context = {
            'medical_history_form': medical_history_form,
            'medical_history': medical_history,
            'add_client_form': add_client_form,
            'client': client,
            'add_doctor_form': add_doctor_form,
            'doctor': doctor,
        }
        return render(request, 'core/pages/medical_history_detail.html', context)

@require_http_methods(['GET', 'POST'])
def treatment(request):
    # Post
    if request.method == 'POST':
        treatment_text = request.POST.get('treatment_text')
        Treatment.objects.create(
            treatment_text=treatment_text,
        )
        return redirect('core:treatment')

    # Get
    context = {
        'treatment_list': Treatment.objects.all(),
    }
    return render(request, 'core/pages/treatment.html', context)

class TreatmentDetailUpdateView(views.View):
    def get(self, request, pk):
        treatment = get_object_or_404(Treatment, pk=pk)
        treatment_form = TreatmentForm(instance=treatment, prefix='treatment')

        add_client_form = AddClientForm(prefix='client')
        add_doctor_form = AddDoctorForm(prefix='doctor')

        client = treatment.client
        doctor = treatment.doctor
        context = {
            'treatment': treatment,
            'treatment_form': treatment_form,
            'add_client_form': add_client_form,
            'client': client,
            'add_doctor_form': add_doctor_form,
            'doctor': doctor,
        }
        return render(request, 'core/pages/treatment_detail.html', context)

    def post(self, request, pk):
        treatment = get_object_or_404(Treatment, pk=pk)
        treatment_form = TreatmentForm(request.POST, instance=treatment, prefix='treatment')

        add_client_form = AddClientForm(request.POST, prefix='client')
        add_doctor_form = AddDoctorForm(request.POST, prefix='doctor')

        client = treatment.client
        doctor = treatment.doctor
        if 'update_treatment' in request.POST:
            if treatment_form.is_valid():
                treatment_form.save()
                return redirect('core:treatment_detail', pk=treatment.pk)
            else:
                print(treatment_form.errors)
        elif 'delete_treatment' in request.POST:
            treatment.delete()
            return redirect('core:treatment')

        elif 'add_client' in request.POST:
            if add_client_form.is_valid():
                select_client = add_client_form.cleaned_data['client']
                treatment.client = select_client
                treatment.save()
                return redirect('core:treatment_detail', pk=treatment.pk)
            else:
                print(add_client_form.errors)
        elif 'delete_client' in request.POST:
            treatment.client = None
            treatment.save()
            return redirect('core:treatment_detail', pk=treatment.pk)
        elif 'delete_doctor' in request.POST:
            treatment.doctor = None
            treatment.save()
            return redirect('core:treatment_detail', pk=treatment.pk)

        elif 'add_doctor' in request.POST:
            if add_doctor_form.is_valid():
                select_doctor = add_doctor_form.cleaned_data['doctor']
                treatment.doctor = select_doctor
                treatment.save()
                return redirect('core:treatment_detail', pk=treatment.pk)
            else:
                print(add_doctor_form.errors)
        context = {
            'treatment_form': treatment_form,
            'treatment': treatment,
            'add_client_form': add_client_form,
            'client': client,
            'add_doctor_form': add_doctor_form,
            'doctor': doctor,
        }
        return render(request, 'core/pages/treatment_detail.html', context)
