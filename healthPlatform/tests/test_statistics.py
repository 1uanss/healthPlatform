import unittest
from src.services.statistics import calculate_statistics
from src.models.patient import Patient

class TestStatistics(unittest.TestCase):

    def setUp(self):
        self.patients = [
            Patient(name="Alice", age=30, phone="1234567890"),
            Patient(name="Bob", age=25, phone="0987654321"),
            Patient(name="Charlie", age=35, phone="1122334455"),
            Patient(name="Diana", age=40, phone="2233445566"),
        ]

    def test_total_patients(self):
        total = calculate_statistics(self.patients)['total']
        self.assertEqual(total, 4)

    def test_average_age(self):
        average_age = calculate_statistics(self.patients)['average_age']
        self.assertEqual(average_age, 32.5)

    def test_youngest_patient(self):
        youngest = calculate_statistics(self.patients)['youngest']
        self.assertEqual(youngest.name, "Bob")

    def test_oldest_patient(self):
        oldest = calculate_statistics(self.patients)['oldest']
        self.assertEqual(oldest.name, "Diana")

if __name__ == '__main__':
    unittest.main()