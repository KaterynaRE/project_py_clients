from datetime import date

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import IntegerChoices, IntegerField

from .doctor import Doctor
from .validators.validators import validate_not_future

class Gender(models.IntegerChoices):
    NOT_SPECIFIED = 0, "Note Specified"
    MALE = 1, "Male"
    FEMALE = 2, "Female"
    OTHER = 3, "Other"

class Client(models.Model):
    #основні поля
    id = models.AutoField(primary_key=True)
    doctors = models.ManyToManyField(Doctor, related_name='clients')
    surname = models.CharField(max_length=50)
    firstname = models.CharField(max_length=50)
    patronymic = models.CharField(max_length=50)
    birthday = models.DateField(validators=[validate_not_future])
    email = models.EmailField()
    gender = IntegerField(choices=Gender.choices)
    #метадані
    created_at = models.DateField(auto_now_add=True) #дані будуть записуватись при створені або передч даних моделі
    updated_at = models.DateField(auto_now=True)

    #методи
    def __str__(self):
        return (f"Id: {self.id}"
                f"Firstname: {self.firstname}"
                f"Surname: {self.surname}"
                f"Email: {self.email}")

