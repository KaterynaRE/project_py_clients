from django.test import  TestCase

from apps.core.models import Doctor


# id = models.AutoField(primary_key=True)
# surname = models.CharField(max_length=50)
# firstname = models.CharField(max_length=50)
# patronymic = models.CharField(max_length=50)

class DoctorModelTest(TestCase):
    def setUp(self):
        """Створення тестового доктора перед тестом"""
        self.doctor_data = {
            'surname': 'Dokt',
            'firstname': 'Ddokt',
            'patronymic': 'DDokt',
        }
        #створення об'єкту доктора, збереження в базу
        self.doctor = Doctor.objects.create(**self.doctor_data)

    def test_create_doctor(self):
        """перевірка що доктор правильно створюється в бд"""
        doctor = Doctor.objects.get(id=self.doctor.id)
        # перевiрка ідентичності через рівність полів
        self.assertEqual(doctor.surname, self.doctor_data['surname'])
        self.assertEqual(doctor.firstname, self.doctor_data['firstname'])
        self.assertEqual(doctor.patronymic, self.doctor_data['patronymic'])


    def test_read_doctor(self):
        """Перевірка, що дані доктора можна коректно прочитати"""
        doctor = Doctor.objects.get(id=self.doctor.id)
        self.assertEqual(doctor.surname, 'Dokt')
        self.assertEqual(doctor.firstname, 'Ddokt')
        self.assertEqual(doctor.patronymic, 'DDokt')

    def test_update_doctor(self):
        """Перевірка, що доктор оновлюється коректно"""
        self.doctor.surname = 'Ivanov'
        self.doctor.firstname = 'Ivan'
        self.doctor.patronymic = 'Ivanovv'
        self.doctor.save()

        update_doctor = Doctor.objects.get(id=self.doctor.id)
        self.assertEqual(update_doctor.surname, 'Ivanov')
        self.assertEqual(update_doctor.firstname, 'Ivan')
        self.assertEqual(update_doctor.patronymic, 'Ivanovv')

    def test_delete_doctor(self):
        """Перевірка, що доктор видаляється коректно"""
        doctor_id = self.doctor.id
        self.doctor.delete()
        with self.assertRaises(Doctor.DoesNotExist):
            Doctor.objects.get(id=doctor_id)

