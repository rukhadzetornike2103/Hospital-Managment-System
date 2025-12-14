
import unittest
from task_model import Task

class TestTaskModel(unittest.TestCase):
    def setUp(self):
        self.task = Task("Clean Room", "2024-04-30", "Pending")

    def test_instance_creation(self):
        self.assertEqual(self.task.description, "Clean Room")
        self.assertEqual(self.task.due_date, "2024-04-30")
        self.assertEqual(self.task.status, "Pending")

if __name__ == '__main__':
    unittest.main()
