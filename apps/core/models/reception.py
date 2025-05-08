from django.db import models
from django.db.models import UniqueConstraint

from apps.core.models.client import Client
from apps.core.models.doctor import Doctor


#прийоми не один
class Reception(models.Model):
    id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='receptions')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='receptions')
    day_to_reception = models.DateTimeField()
    reason_for_request = models.CharField(max_length=200)

    #для уникнення дублювання
    class Meta:
        unique_reception = [
            UniqueConstraint('client', 'doctor', 'day_to_reception', 'reason_for_request')
        ]

    def __str__(self):
        return (f"Reception: {self.id} for {self.client}"
                f"Day to reception: {self.day_to_reception}"
                f"Reason: {self.reason_for_request}"
                f"Doctor: {self.doctor}")