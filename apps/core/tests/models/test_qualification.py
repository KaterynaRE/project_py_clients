import os
import sys
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from django.test import  TestCase
from apps.core.models import Qualification

# id = models.AutoField(primary_key=True)
# qualification_name = models.CharField(max_length=50, unique=True)

class QualificationModelTest(TestCase):
    def setUp(self):
        """Створення тестового Qualification перед тестом"""
        self.qualification_data = {
            'qualification_name': 'Cardiology',
        }
        #створення об'єкту Qualification, збереження в базу
        self.qualification = Qualification.objects.create(**self.qualification_data)

    def test_create_qualification(self):
        """перевірка що qualification правильно створюється в бд"""
        qualification = Qualification.objects.get(id=self.qualification.id)
        # перевiрка ідентичності через рівність полів
        self.assertEqual(qualification.qualification_name, self.qualification_data['qualification_name'])


    def test_read_qualification(self):
        """Перевірка, що дані qualification можна коректно прочитати"""
        qualification = Qualification.objects.get(id=self.qualification.id)
        self.assertEqual(qualification.qualification_name, 'Cardiology')

    def test_update_qualification(self):
        """Перевірка, що qualification оновлюється коректно"""
        self.qualification.qualification_name = 'Nevrolog'
        self.qualification.save()

        update_qualification = Qualification.objects.get(id=self.qualification.id)
        self.assertEqual(update_qualification.qualification_name, 'Nevrolog')

    def test_delete_qualification(self):
        """Перевірка, що qualification видаляється коректно"""
        qualification_id = self.qualification.id
        self.qualification.delete()
        with self.assertRaises(Qualification.DoesNotExist):
            Qualification.objects.get(id=qualification_id)