
import unittest
from payment_method import PaymentMethod

class TestPaymentMethod(unittest.TestCase):
    def setUp(self):
        self.payment_method = PaymentMethod("Visa", "Credit Card")

    def test_instance_creation(self):
        self.assertEqual(self.payment_method.type, "Visa")
        self.assertEqual(self.payment_method.method, "Credit Card")

if __name__ == '__main__':
    unittest.main()
