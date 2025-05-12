from django.db import models

#треба заборонити щоб не можна було створити таблицю, на основі цього базового класу
class TimeStampedModel(models.Model):
    #метадані
    created_at = models.DateField(auto_now_add=True) #дані будуть записуватись при створені або передч даних моделі
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return (f"{self.created_at} "
                f"{self.updated_at}")

    class Meta:
        #не створює таблиці в БД
        abstract = True