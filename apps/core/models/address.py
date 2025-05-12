from django.db import models


class Address(models.Model):
    id = models.BigAutoField(primary_key=True)
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    house = models.CharField(max_length=50)
    apartment = models.CharField(max_length=50)

    def __str__(self):
        return (f"Id: {self.id}"
                f"City: {self.city}"
                f"Street: {self.street}"
                f"House: {self.house}"
                f"Apartment: {self.apartment}")