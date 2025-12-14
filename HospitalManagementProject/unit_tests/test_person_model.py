
import unittest
from person_model import Person

class TestPersonModel(unittest.TestCase):
    def setUp(self):
        self.person = Person("Alice Johnson", 30)

    def test_instance_creation(self):
        self.assertEqual(self.person.name, "Alice Johnson")
        self.assertEqual(self.person.age, 30)

if __name__ == '__main__':
    unittest.main()
