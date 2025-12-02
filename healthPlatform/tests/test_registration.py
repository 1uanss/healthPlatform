import unittest
from src.services.registration import register_patient, validate_patient_data
from src.models.patient import Patient

class TestPatientRegistration(unittest.TestCase):

    def test_register_patient_valid(self):
        patient_data = {
            'name': 'John Doe',
            'age': 30,
            'phone': '123-456-7890'
        }
        patient = register_patient(patient_data)
        self.assertIsInstance(patient, Patient)
        self.assertEqual(patient.name, patient_data['name'])
        self.assertEqual(patient.age, patient_data['age'])
        self.assertEqual(patient.phone, patient_data['phone'])

    def test_register_patient_invalid_age(self):
        patient_data = {
            'name': 'Jane Doe',
            'age': -5,
            'phone': '123-456-7890'
        }
        with self.assertRaises(ValueError):
            register_patient(patient_data)

    def test_validate_patient_data_valid(self):
        patient_data = {
            'name': 'John Doe',
            'age': 30,
            'phone': '123-456-7890'
        }
        self.assertTrue(validate_patient_data(patient_data))

    def test_validate_patient_data_missing_name(self):
        patient_data = {
            'age': 30,
            'phone': '123-456-7890'
        }
        self.assertFalse(validate_patient_data(patient_data))

    def test_validate_patient_data_invalid_phone(self):
        patient_data = {
            'name': 'John Doe',
            'age': 30,
            'phone': 'invalid-phone'
        }
        self.assertFalse(validate_patient_data(patient_data))

if __name__ == '__main__':
    unittest.main()