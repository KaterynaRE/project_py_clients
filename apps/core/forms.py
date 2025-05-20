from django import forms

from apps.core.models import Client


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
            'birthday': forms.DateInput(attrs={'type':'date', 'class':'form-control'}, format='%Y-%m-%d')
        }
