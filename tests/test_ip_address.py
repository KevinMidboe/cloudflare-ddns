import unittest
from src.main import validIP

MOCK_IP = "44.208.147.61"


class TestIPAddress(unittest.TestCase):
    def test_valid_ip(self):
        self.assertTrue(validIP(MOCK_IP))

    def test_invalid_ip(self):
        ip = "256.0.0.1"
        self.assertFalse(validIP(ip))

    def test_invalid_format(self):
        ip = "192.168.1"
        self.assertFalse(validIP(ip))

    def test_empty_string(self):
        ip = ""
        self.assertFalse(validIP(ip))

    def test_error_looking_string(self):
        ip = "upstream connect error or disconnect/reset before headers. reset reason: connection timeout."
        self.assertFalse(validIP(ip))

    def test_none(self):
        ip = None
        self.assertFalse(validIP(ip))


if __name__ == "__main__":
    unittest.main()
