
import unittest
from outpatient_model import Outpatient

class TestOutpatientModel(unittest.TestCase):
    def setUp(self):
        self.outpatient = Outpatient("John Smith", "2024-04-28", "General Checkup")

    def test_instance_creation(self):
        self.assertEqual(self.outpatient.name, "John Smith")
        self.assertEqual(self.outpatient.date, "2024-04-28")
        self.assertEqual(self.outpatient.reason, "General Checkup")

if __name__ == '__main__':
    unittest.main()
