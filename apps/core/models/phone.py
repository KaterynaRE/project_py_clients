from django.db import models


class Phone(models.Model):
    id = models.BigAutoField(primary_key=True)
    phone_number = models.CharField(max_length=15)

    # client.phones.all()
    client = models.ForeignKey('Client', on_delete=models.CASCADE, related_name='phones')
    def __str__(self):
        return (f"{self.id}"
                f"{self.phone_number}")
