from django.db import models

#план лікування
class Treatment(models.Model):
    id = models.BigAutoField(primary_key=True)
    treatment_text = models.CharField(max_length=500)

    client = models.ForeignKey('Client', on_delete=models.CASCADE, related_name='treatments')
    history = models.ForeignKey('MedicalHistory', on_delete=models.CASCADE, related_name='treatments')
    doctor = models.ForeignKey('Doctor', on_delete=models.SET_NULL, null=True, blank=True,related_name='treatments')

    def __str__(self):
        return (f"id: {self.id}"
                f"appointment: {self.treatment_text}")