import unittest
import responses
from src.main import publicAddress

MOCK_IP = '44.208.147.61'
MOCK_TIMEOUT = 'upstream connect error or disconnect/reset before headers. reset reason: connection timeout.'


class TestPublicAddress(unittest.TestCase):

    @responses.activate
    def test_successfull_response(self):
        responses.add(responses.GET, 'https://ifconfig.me',
                      body=MOCK_IP, status=200)

        ip = publicAddress()

        self.assertEqual(MOCK_IP, ip)

    @responses.activate
    def test_timeout_response(self):
        responses.add(responses.GET, 'https://ifconfig.me',
                      body=MOCK_TIMEOUT, status=500)

        ip = publicAddress()

        self.assertIsNone(ip)

    @responses.activate
    def test_mangled_response(self):
        responses.add(responses.GET, 'https://ifconfig.me',
                      body='123.22', status=200)

        ip = publicAddress()

        self.assertIsNone(ip)


if __name__ == '__main__':
    unittest.main()
