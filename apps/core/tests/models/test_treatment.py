import os
import sys
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from django.test import  TestCase
from apps.core.models import Treatment

# id = models.BigAutoField(primary_key=True)
#     treatment_text = models.CharField(max_length=500)

class TreatmentModelTest(TestCase):
    def setUp(self):
        """Створення тестового Treatment перед тестом"""
        self.treatment_data = {
            'treatment_text': 'Tratara',
        }
        #створення об'єкту Treatment, збереження в базу
        self.treatment = Treatment.objects.create(**self.treatment_data)

    def test_create_treatment(self):
        """перевірка що treatment правильно створюється в бд"""
        treatment = Treatment.objects.get(id=self.treatment.id)
        # перевiрка ідентичності через рівність полів
        self.assertEqual(treatment.treatment_text, self.treatment_data['treatment_text'])


    def test_read_treatment(self):
        """Перевірка, що дані treatment можна коректно прочитати"""
        treatment = Treatment.objects.get(id=self.treatment.id)
        self.assertEqual(treatment.treatment_text, 'Tratara')

    def test_update_treatment(self):
        """Перевірка, що treatment оновлюється коректно"""
        self.treatment.treatment_text = 'NewNew'
        self.treatment.save()

        update_treatment = Treatment.objects.get(id=self.treatment.id)
        self.assertEqual(update_treatment.treatment_text, 'NewNew')

    def test_delete_treatment(self):
        """Перевірка, що treatment видаляється коректно"""
        treatment_id = self.treatment.id
        self.treatment.delete()
        with self.assertRaises(Treatment.DoesNotExist):
            Treatment.objects.get(id=treatment_id)