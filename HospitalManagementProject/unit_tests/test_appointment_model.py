
import unittest
from appointment_model import Appointment


class TestAppointmentModel(unittest.TestCase):
    def setUp(self):
        self.appointment = Appointment("2024-04-28", "Doctor Who", "John Smith")

    def test_instance_creation(self):
        self.assertEqual(self.appointment.date, "2024-04-28")
        self.assertEqual(self.appointment.doctor, "Doctor Who")
        self.assertEqual(self.appointment.patient, "John Smith")


if __name__ == '__main__':
    unittest.main()
