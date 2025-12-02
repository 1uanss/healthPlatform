import unittest
from src.models.patient import Patient
from src.services.search import search_patient_by_name

class TestPatientSearch(unittest.TestCase):

    def setUp(self):
        self.patients = [
            Patient(name="John Doe", age=30, phone_number="123-456-7890"),
            Patient(name="Jane Smith", age=25, phone_number="987-654-3210"),
            Patient(name="Alice Johnson", age=40, phone_number="555-555-5555"),
        ]

    def test_search_existing_patient(self):
        result = search_patient_by_name(self.patients, "Jane Smith")
        self.assertEqual(result.name, "Jane Smith")
        self.assertEqual(result.age, 25)
        self.assertEqual(result.phone_number, "987-654-3210")

    def test_search_non_existing_patient(self):
        result = search_patient_by_name(self.patients, "Bob Brown")
        self.assertIsNone(result)

    def test_search_case_insensitive(self):
        result = search_patient_by_name(self.patients, "alice johnson")
        self.assertEqual(result.name, "Alice Johnson")
        self.assertEqual(result.age, 40)
        self.assertEqual(result.phone_number, "555-555-5555")

if __name__ == '__main__':
    unittest.main()