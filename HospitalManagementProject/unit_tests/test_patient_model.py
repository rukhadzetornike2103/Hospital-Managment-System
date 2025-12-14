
import unittest
from patient_model import Patient

class TestPatientModel(unittest.TestCase):
    def setUp(self):
        self.patient = Patient("Jane Doe", 12345, "Emergency")

    def test_instance_creation(self):
        self.assertEqual(self.patient.name, "Jane Doe")
        self.assertEqual(self.patient.patient_id, 12345)
        self.assertEqual(self.patient.department, "Emergency")

if __name__ == '__main__':
    unittest.main()
