from django.db import models


class MedicalHistory(models.Model):
    id = models.BigAutoField(primary_key=True)
    name_of_disease = models.CharField(max_length=200)
    diagnostic_date = models.DateField()
    is_chronic = models.BooleanField(default=False)

    client = models.ForeignKey('Client', on_delete=models.CASCADE, related_name='medical_histories')
    doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE, related_name='medical_histories')
    treatment = models.ForeignKey('Treatment', on_delete=models.CASCADE, related_name='medical_histories')
    def __str__(self):
        return (f"Id: {self.id} "
                f"Disease: {self.name_of_disease} {'chronic' if self.is_chronic else 'acute'}"
                f"Diagnostic date: {self.diagnostic_date}")
