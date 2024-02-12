import re
import unittest
import responses
from src.main import cloudflareDDNS

MOCK_IP = '44.208.147.61'
CLOUDFLARE_GET_RECORDS_URL = re.compile(
    r"https\:\/\/api.cloudflare.com\/client\/v4\/zones\/\w*\/dns_records\?type\=A")
CLOUDFLARE_ADDR_RECORD_EXISTS_RESPONSE = {
    'success': True,
    'result': [{
        'content': MOCK_IP,
        'name': 'addr.',
        'id': 'id',
        'ttl': 86400,
        'proxied': True
    }]
}
CLOUDFLARE_ADDR_RECORD_NONEXISTANT_RESPONSE = {
    'success': True,
    'result': [{
        'content': MOCK_IP,
        'name': None,
        'id': 'id',
        'ttl': 86400,
        'proxied': True
    }]
}
CLOUDFLARE_500_RESPONSE = {
    'success': False,
    'errors': 'someerror'
}


class TestCloudflareDNSRecordIP(unittest.TestCase):

    @responses.activate
    def test_successfull_response(self):
        responses.add(responses.GET, CLOUDFLARE_GET_RECORDS_URL,
                      json=CLOUDFLARE_ADDR_RECORD_EXISTS_RESPONSE, status=200)

        ip = cloudflareDDNS()

        self.assertEqual(MOCK_IP, ip)

    @responses.activate
    def test_addr_record_exists(self):
        responses.add(responses.GET, CLOUDFLARE_GET_RECORDS_URL,
                      json=CLOUDFLARE_ADDR_RECORD_NONEXISTANT_RESPONSE,
                      status=200)

        self.assertRaises(Exception, cloudflareDDNS)

    @responses.activate
    def test_cloudflare_500_response(self):
        responses.add(responses.GET, CLOUDFLARE_GET_RECORDS_URL,
                      json=CLOUDFLARE_500_RESPONSE,
                      status=500)

        self.assertRaises(Exception, cloudflareDDNS)

    @responses.activate
    def test_cloudflare_empty_200_response(self):
        responses.add(responses.GET, CLOUDFLARE_GET_RECORDS_URL,
                      json={},
                      status=500)

        self.assertRaises(Exception, cloudflareDDNS)

    @responses.activate
    def test_cloudflare_empty_500_response(self):
        responses.add(responses.GET, CLOUDFLARE_GET_RECORDS_URL,
                      json={},
                      status=500)

        self.assertRaises(Exception, cloudflareDDNS)


if __name__ == '__main__':
    unittest.main()
