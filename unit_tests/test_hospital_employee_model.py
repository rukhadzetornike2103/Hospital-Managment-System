
import unittest
from hospital_employee_model import HospitalEmployee

class TestHospitalEmployeeModel(unittest.TestCase):
    def setUp(self):
        self.employee = HospitalEmployee(1, "Alice Johnson", "Administration")

    def test_instance_creation(self):
        self.assertEqual(self.employee.employee_id, 1)
        self.assertEqual(self.employee.name, "Alice Johnson")
        self.assertEqual(self.employee.department, "Administration")

if __name__ == '__main__':
    unittest.main()
