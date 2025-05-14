import os
import sys
import django


# sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
# django.setup()

from datetime import date

from django.test import  TestCase

from apps.core.models.client import Gender, Client


class ClientModelTest(TestCase):
    def setUp(self):
        """Створення тестового клієнта перед тестом"""
        self.client_data = {
            'surname': 'And',
            'firstname': 'Oko',
            'patronymic': 'Vit',
            'birthday': date(1994, 11, 12),
            'email': 'qwwr@.gmail.com',
            'gender': Gender.MALE
        }
        #створення об'єкту клієнта, збереження в базу
        self.client = Client.objects.create(**self.client_data)

    def test_create_client(self):
        """перевірка що клієнт правильно створюється в бд"""
        client = Client.objects.get(id=self.client.id)
        #перевiрка ідентичності через рівність полів
        #1
        self.assertEqual(client.surname, self.client_data['surname'])
        self.assertEqual(client.firstname, self.client_data['firstname'])
        self.assertEqual(client.patronymic, self.client_data['patronymic'])
        self.assertEqual(client.birthday, self.client_data['birthday'])
        self.assertEqual(client.email, self.client_data['email'])
        self.assertEqual(client.gender, self.client_data['gender'])

        #2 тільки тоді реалізований метод __eq__ __hash__ в моделі
        #self.assertEqual(client, self.client)

    def test_read_client(self):
        """Перевірка, що дані клієнта можна коректно прочитати"""
        client = Client.objects.get(id=self.client.id)
        self.assertEqual(client.surname, 'And')
        self.assertEqual(client.firstname, 'Oko')
        self.assertEqual(client.patronymic, 'Vit')
        self.assertEqual(client.birthday, date(1994, 11, 12))
        self.assertEqual(client.email, 'qwwr@.gmail.com')
        self.assertEqual(client.gender, Gender.MALE)

    def test_update_client(self):
        """Перевірка, що клієнт оновлюється коректно"""
        self.client.surname = 'John'
        self.client.firstname = 'Mihael'
        self.client.save()

        update_client = Client.objects.get(id=self.client.id)
        self.assertEqual(update_client.surname, 'John')
        self.assertEqual(update_client.firstname, 'Mihael')

    def test_delete_client(self):
        """Перевірка, що клієнт видаляється коректно"""
        client_id = self.client.id
        self.client.delete()
        with self.assertRaises(Client.DoesNotExist):
            Client.objects.get(id=client_id)
