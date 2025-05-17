import os
import sys
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from datetime import  date
from django.test import  TestCase
from apps.core.models import MedicalHistory

# id = models.BigAutoField(primary_key=True)
# name_of_disease = models.CharField(max_length=200)
# diagnostic_date = models.DateField()
# is_chronic = models.BooleanField(default=False)

class MedicalHistoryModelTest(TestCase):
    def setUp(self):
        """Створення тестового MedicalHistory перед тестом"""
        self.medical_history_data = {
            'name_of_disease': 'Flu',
            'diagnostic_date': date(2025, 11, 12),
            'is_chronic': False,
        }
        #створення об'єкту medical_history, збереження в базу
        self.medical_history = MedicalHistory.objects.create(**self.medical_history_data)

    def test_create_medical_history(self):
        """перевірка що medical_history правильно створюється в бд"""
        medical_history = MedicalHistory.objects.get(id=self.medical_history.id)
        # перевiрка ідентичності через рівність полів
        self.assertEqual(medical_history.name_of_disease, self.medical_history_data['name_of_disease'])
        self.assertEqual(medical_history.diagnostic_date, self.medical_history_data['diagnostic_date'])
        self.assertEqual(medical_history.is_chronic, self.medical_history_data['is_chronic'])


    def test_read_medical_history(self):
        """Перевірка, що дані medical_history можна коректно прочитати"""
        medical_history = MedicalHistory.objects.get(id=self.medical_history.id)
        self.assertEqual(medical_history.name_of_disease, 'Flu')
        self.assertEqual(medical_history.diagnostic_date, date(2025, 11, 12))
        self.assertEqual(medical_history.is_chronic, False)

    def test_update_medical_history(self):
        """Перевірка, що medical_history оновлюється коректно"""
        self.medical_history.name_of_disease = 'XA'
        self.medical_history.diagnostic_date = date(2025, 5, 12)
        self.medical_history.save()

        update_medical_history = MedicalHistory.objects.get(id=self.medical_history.id)
        self.assertEqual(update_medical_history.name_of_disease, 'XA')
        self.assertEqual(update_medical_history.diagnostic_date, date(2025, 5, 12))

    def test_delete_medical_history(self):
        """Перевірка, що medical_history видаляється коректно"""
        medical_history_id = self.medical_history.id
        self.medical_history.delete()
        with self.assertRaises(MedicalHistory.DoesNotExist):
            MedicalHistory.objects.get(id=medical_history_id)

