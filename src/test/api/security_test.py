import unittest
from api.security import hash, secret_is_valid


class SecurityTest(unittest.TestCase):
    def test_secret_is_valid_when_valid(self):
        secret = "my_secret"
        hashed_secret = hash(secret)
        self.assertTrue(secret_is_valid(secret, hashed_secret))

    def test_secret_is_valid_when_invalid(self):
        secret = "my_secret"
        with self.assertRaises(ValueError):
            self.assertTrue(secret_is_valid(secret, "my_secret"))


if __name__ == '__main__':
    unittest.main()
