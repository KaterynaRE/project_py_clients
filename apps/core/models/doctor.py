from django.db import models

from apps.core.models.client import Client


class Doctor(models.Model):
    id = models.AutoField(primary_key=True)
    clients = models.ManyToManyField(Client, related_name='doctors')
    surname = models.CharField(max_length=50)
    firstname = models.CharField(max_length=50)
    patronymic = models.CharField(max_length=50)
    qualification = models.CharField(max_length=50)

    def __str__(self):
        return (f"Id: {self.id}"
                f" {self.surname} "
                f"{self.firstname}"
                f" {self.patronymic} - qualification: {self.qualification}")