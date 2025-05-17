import os
import sys
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from datetime import  date
from django.test import  TestCase
from apps.core.models.client import Gender
from apps.core.models import Client, Phone


# id = models.BigAutoField(primary_key=True)
# phone_number = models.CharField(max_length=15)

class PhoneModelTest(TestCase):
    def setUp(self):
        """Створення тестового Phone перед тестом"""
        self.phone_data = {
            'phone_number': '123456890',
        }
        #створення об'єкту phone, збереження в базу
        self.phone = Phone.objects.create(**self.phone_data)

    def test_create_phone(self):
        """перевірка що phone правильно створюється в бд"""
        phone = Phone.objects.get(id=self.phone.id)
        # перевiрка ідентичності через рівність полів
        self.assertEqual(phone.phone_number, self.phone_data['phone_number'])

    def test_read_phone(self):
        """Перевірка, що дані phone можна коректно прочитати"""
        phone = Phone.objects.get(id=self.phone.id)
        self.assertEqual(phone.phone_number, '123456890')

    def test_update_phone(self):
        """Перевірка, що phone оновлюється коректно"""
        self.phone.phone_number = '444456890'
        self.phone.save()

        update_phone = Phone.objects.get(id=self.phone.id)
        self.assertEqual(update_phone.phone_number, '444456890')

    def test_delete_phone(self):
        """Перевірка, що phone видаляється коректно"""
        phone_id = self.phone.id
        self.phone.delete()
        with self.assertRaises(Phone.DoesNotExist):
            Phone.objects.get(id=phone_id)