from django.db import models

from apps.core.models.appointment import Appointment
from apps.core.models.client import Client
from apps.core.models.doctor import Doctor


class MedicalHistory(models.Model):
    id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='medical_histories')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='medical_histories')
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='medical_histories')
    name_of_disease = models.CharField(max_length=200)
    diagnostic_date = models.DateField()
    is_chronic = models.BooleanField(default=False)

    def __str__(self):
        return (f"Id: {self.id} for patient {self.client}"
                f"Disease: {self.name_of_disease} {'chronic' if self.is_chronic else 'acute'}"
                f"Diagnostic date: {self.diagnostic_date}"
                f"Doctor: {self.doctor}"
                f"Appointment: {self.appointment}")