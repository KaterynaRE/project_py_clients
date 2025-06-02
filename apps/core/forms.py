from django import forms

from apps.core.models import Client, Address, Doctor, Phone, Qualification, Appointment


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        #вибрані поля
        #fields = ['surname', 'firstname', 'patronymic']
        # all pola
        fields = '__all__'
        exclude = ['doctors', 'address', 'created_at', 'updated_at']
        #налаштування полів
        widgets = {
            'surname': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Surname'}),
            'birthday': forms.DateInput(attrs={'type':'date', 'class':'form-control'}, format='%Y-%m-%d')
        }

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = '__all__'
        exclude = ['created_at', 'updated_at']


class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = '__all__'
        exclude = ['created_at', 'updated_at']
        widgets = {
            'surname': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Surname'}),
        }

class QualificationForm(forms.ModelForm):
    class Meta:
        model = Qualification
        fields = '__all__'
        exclude = ['created_at', 'updated_at', 'doctor']


class PhoneForm(forms.ModelForm):
    class Meta:
        model = Phone
        fields = '__all__'
        exclude = ['created_at', 'updated_at', 'client']

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = '__all__'
        exclude = ['created_at', 'updated_at', 'client', 'doctor']
