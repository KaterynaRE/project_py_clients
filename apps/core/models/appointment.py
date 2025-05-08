from django.db import models

from apps.core.models.client import Client
from apps.core.models.doctor import Doctor
from apps.core.models.medical_history import MedicalHistory

#план лікування
class Appointment(models.Model):
    id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='appointments')
    history = models.ForeignKey(MedicalHistory, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, related_name='appointments')
    appointment_text = models.CharField(max_length=500)

    def __str__(self):
        return (f"id: {self.id} for patient {self.client}"
                f"doctor: {self.doctor}"
                f"medical history: {self.history}"
                f"appointment: {self.appointment_text}")