import unittest
from validation import register_user_validation
from database.user import login_user


class TestUser(unittest.TestCase):
    def test_register(self):
        msg1 = register_user_validation(
            username='Mohammad', password='abc123456')
        msg2 = register_user_validation(username='Danial', password='12345678')
        msg3 = register_user_validation(username='Mohammad', password='123abc')
        msg4 = register_user_validation(username='Mosfazli', password='abcd')
        msg5 = register_user_validation(username='DtechB', password='454545')
        msg6 = register_user_validation(username='Ali', password='87654321')
        msg7 = register_user_validation(username='Ahmad', password='111111')
        msg8 = register_user_validation(username='Reza', password='123')

        self.assertEqual(msg1, 'success')
        self.assertEqual(msg2, 'success')
        self.assertEqual(msg3, 'success')
        self.assertEqual(msg4, 'success')
        self.assertEqual(msg5, 'success')
        self.assertEqual(msg6, 'success')
        self.assertEqual(msg7, 'success')
        self.assertEqual(msg8, 'success')
        self.assertTrue(len('ad') >= 3)
        self.assertTrue(len('ad') >= 3)
        self.assertTrue(len('Mahmud') >= 3)

    def test_login(self):
        msg1 = login_user(
            username='DtechB', password='12345678')
        msg2 = login_user(username='Ali', password='12345678')

        self.assertTrue(msg1.find('Connected') != -1)
        self.assertTrue(msg2.find('Connected') != -1)


if __name__ == '__main__':
    unittest.main()
