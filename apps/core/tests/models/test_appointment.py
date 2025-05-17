import os
import sys
import django
from django.utils.timezone import make_aware

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from datetime import datetime, date
from django.test import  TestCase
from apps.core.models import Appointment, Client, Doctor

# id = models.BigAutoField(primary_key=True)
# day_to_appointment = models.DateTimeField()
# reason_for_request = models.CharField(max_length=200)


class AppointmentModelTest(TestCase):
    def setUp(self):
        """Створення тестового Appointment перед тестом"""
        self.appointment_data = {
            'day_to_appointment': make_aware(datetime(2025, 11, 12, 11, 30)),
            'reason_for_request': 'heat',
            # 'client': self.client_data,
            # 'doctor': self.doctor_data
        }
        #створення об'єкту appointment, збереження в базу
        self.appointment = Appointment.objects.create(**self.appointment_data)

    def test_create_appointment(self):
        """перевірка що appointment правильно створюється в бд"""
        appointment = Appointment.objects.get(id=self.appointment.id)
        # перевiрка ідентичності через рівність полів
        self.assertEqual(appointment.day_to_appointment, self.appointment_data['day_to_appointment'])
        self.assertEqual(appointment.reason_for_request, self.appointment_data['reason_for_request'])

    def test_read_appointment(self):
        """Перевірка, що дані appointment можна коректно прочитати"""
        appointment = Appointment.objects.get(id=self.appointment.id)
        self.assertEqual(appointment.day_to_appointment,  make_aware(datetime(2025, 11, 12, 11, 30)))
        self.assertEqual(appointment.reason_for_request, 'heat')

    def test_update_appointment(self):
        """Перевірка, що appointment оновлюється коректно"""
        self.appointment.day_to_appointment = make_aware(datetime(2025, 5, 12, 11, 30))
        self.appointment.reason_for_request = 'heat'
        self.appointment.save()

        update_appointment = Appointment.objects.get(id=self.appointment.id)
        self.assertEqual(update_appointment.day_to_appointment, make_aware(datetime(2025, 5, 12, 11, 30)))
        self.assertEqual(update_appointment.reason_for_request, 'heat')

    def test_delete_appointment(self):
        """Перевірка, що appointment видаляється коректно"""
        appointment_id = self.appointment.id
        self.appointment.delete()
        with self.assertRaises(Appointment.DoesNotExist):
            Appointment.objects.get(id=appointment_id)

