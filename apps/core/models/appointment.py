from django.db import models
from django.db.models import UniqueConstraint

#прийоми не один
class Appointment(models.Model):
    id = models.BigAutoField(primary_key=True)
    day_to_appointment = models.DateTimeField()
    reason_for_request = models.CharField(max_length=200)

    client = models.ForeignKey('Client', on_delete=models.CASCADE, related_name='appointments', null=True, blank=True)
    doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE, related_name='appointments', null=True, blank=True)
    #для уникнення дублювання
    class Meta:
        constraints = [
            UniqueConstraint(fields=['client', 'doctor', 'day_to_appointment', 'reason_for_request'],
                             name='unique_client_doctor')
        ]

    def __str__(self):
        return (f"Reception: {self.id}"
                f"Day to reception: {self.day_to_appointment}"
                f"Reason: {self.reason_for_request}")
