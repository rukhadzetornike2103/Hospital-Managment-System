
import unittest
from nurse_model import Nurse

class TestNurseModel(unittest.TestCase):
    def setUp(self):
        self.nurse = Nurse(10, "Mary Poppins", "Registered Nurse")

    def test_instance_creation(self):
        self.assertEqual(self.nurse.nurse_id, 10)
        self.assertEqual(self.nurse.name, "Mary Poppins")
        self.assertEqual(self.nurse.qualifications, "Registered Nurse")

if __name__ == '__main__':
    unittest.main()
