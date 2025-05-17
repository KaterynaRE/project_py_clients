from django.db import models


class Qualification(models.Model):
    id = models.AutoField(primary_key=True)
    qualification_name = models.CharField(max_length=50, unique=True)

    doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE, related_name='qualifications', null=True, blank=True)
    def __str__(self):
        return f"id: {self.id} - qualification name: {self.qualification_name}"