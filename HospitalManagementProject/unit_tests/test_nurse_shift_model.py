
import unittest
from nurse_shift_model import NurseShift

class TestNurseShiftModel(unittest.TestCase):
    def setUp(self):
        self.nurse_shift = NurseShift(10, "2024-04-28", "Night")

    def test_instance_creation(self):
        self.assertEqual(self.nurse_shift.nurse_id, 10)
        self.assertEqual(self.nurse_shift.date, "2024-04-28")
        self.assertEqual(self.nurse_shift.shift_type, "Night")

if __name__ == '__main__':
    unittest.main()
