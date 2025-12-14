
import unittest
from inpatient_model import Inpatient

class TestInpatientModel(unittest.TestCase):
    def setUp(self):
        self.inpatient = Inpatient(101, 507, "2024-04-20")

    def test_instance_creation(self):
        self.assertEqual(self.inpatient.patient_id, 101)
        self.assertEqual(self.inpatient.room_number, 507)
        self.assertEqual(self.inpatient.admission_date, "2024-04-20")

if __name__ == '__main__':
    unittest.main()
