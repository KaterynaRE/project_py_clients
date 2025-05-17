import os
import sys
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from django.test import  TestCase
from apps.core.models import Address

# id = models.BigAutoField(primary_key=True)
# city = models.CharField(max_length=50)
# street = models.CharField(max_length=50)
# house = models.CharField(max_length=50)
# apartment = models.CharField(max_length=50)

class AddressModelTest(TestCase):
    def setUp(self):
        """Створення тестового Address перед тестом"""
        self.address_data = {
            'city': 'Kush',
            'street': 'Peremogy',
            'house': '33',
            'apartment': '-',
        }
        #створення об'єкту Address, збереження в базу
        self.address = Address.objects.create(**self.address_data)

    def test_create_address(self):
        """перевірка що address правильно створюється в бд"""
        address = Address.objects.get(id=self.address.id)
        # перевiрка ідентичності через рівність полів
        self.assertEqual(address.city, self.address_data['city'])
        self.assertEqual(address.street, self.address_data['street'])
        self.assertEqual(address.house, self.address_data['house'])
        self.assertEqual(address.apartment, self.address_data['apartment'])


    def test_read_address(self):
        """Перевірка, що дані address можна коректно прочитати"""
        address = Address.objects.get(id=self.address.id)
        self.assertEqual(address.city, 'Kush')
        self.assertEqual(address.street, 'Peremogy')
        self.assertEqual(address.house, '33')
        self.assertEqual(address.apartment, '-')

    def test_update_address(self):
        """Перевірка, що address оновлюється коректно"""
        self.address.city = 'Zp'
        self.address.street = 'Komar'
        self.address.house = '27'
        self.address.save()

        update_address = Address.objects.get(id=self.address.id)
        self.assertEqual(update_address.city, 'Zp')
        self.assertEqual(update_address.street, 'Komar')
        self.assertEqual(update_address.house, '27')

    def test_delete_address(self):
        """Перевірка, що address видаляється коректно"""
        address_id = self.address.id
        self.address.delete()
        with self.assertRaises(Address.DoesNotExist):
            Address.objects.get(id=address_id)

