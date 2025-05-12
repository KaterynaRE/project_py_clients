
from django.db import models
from django.db.models import IntegerChoices, IntegerField

from .base_models import TimeStampedModel
from .validators.validators import validate_not_future

class Gender(models.IntegerChoices):
    NOT_SPECIFIED = 0, "Note Specified"
    MALE = 1, "Male"
    FEMALE = 2, "Female"
    OTHER = 3, "Other"

# class Client(models.Model):
class Client(TimeStampedModel):
    #метадані будуть тут

    #основні поля
    id = models.BigAutoField(primary_key=True)
    surname = models.CharField(max_length=50)
    firstname = models.CharField(max_length=50)
    patronymic = models.CharField(max_length=50)
    birthday = models.DateField(validators=[validate_not_future])
    email = models.EmailField()
    gender = IntegerField(choices=Gender.choices)
    # #метадані
    # created_at = models.DateField(auto_now_add=True) #дані будуть записуватись при створені або передч даних моделі
    # updated_at = models.DateField(auto_now=True)

    doctors = models.ManyToManyField('Doctor', related_name='clients')
    address = models.OneToOneField('Address', related_name='clients', on_delete=models.SET_NULL, null=True, blank=True)

    #методи
    def __str__(self):
        return (f"Id: {self.id}"
                f"{self.firstname}"
                f"{self.surname}"
                f"{self.patronymic}"
                f"{self.birthday}"
                f"{self.email}"
                f"{self.gender}"
                f"{super().__str__()}")

