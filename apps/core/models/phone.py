from django.db import models

from apps.core.models.client import Client


class Phone(models.Model):
    id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='phones')
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.phone_number}: {self.client}"