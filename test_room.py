import unittest
from client import Client
from menu import choose_room


class TestRoom(unittest.TestCase):
    def test_choosing_room(self):
        cli1 = Client('127.0.0.1', 50000)

        option = choose_room()
        if option == 1:
            cli1.roomName = 'Computer'
        else:
            cli1.roomName = 'Wrong'

        self.assertEqual(cli1.roomName, 'Computer')


if __name__ == '__main__':
    unittest.main()
