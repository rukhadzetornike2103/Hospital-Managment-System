
import unittest
from room_model import Room

class TestRoomModel(unittest.TestCase):
    def setUp(self):
        self.room = Room(101, "Single", "Available")

    def test_instance_creation(self):
        self.assertEqual(self.room.room_number, 101)
        self.assertEqual(self.room.room_type, "Single")
        self.assertEqual(self.room.status, "Available")

if __name__ == '__main__':
    unittest.main()
