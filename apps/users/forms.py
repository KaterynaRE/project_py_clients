from django.contrib.auth.forms import UserCreationForm

from apps.users.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': field.label
            })

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')
