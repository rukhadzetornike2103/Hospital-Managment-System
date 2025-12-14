
import unittest
from doctor_model import Doctor

class TestDoctorModel(unittest.TestCase):
    def setUp(self):
        self.doctor = Doctor("John Doe", "Cardiology")

    def test_instance_creation(self):
        self.assertEqual(self.doctor.name, "John Doe")
        self.assertEqual(self.doctor.specialization, "Cardiology")

    def test_str_method(self):
        self.assertEqual(str(self.doctor), "Doctor John Doe, Specialization: Cardiology")

if __name__ == '__main__':
    unittest.main()
