import os
import requests
from bulk_dns_update import updateAllZones, setAPIKey, getDDNSAddresszoneId
from dotenv import load_dotenv

load_dotenv()

currentIP = None
DDNS_ZONE = os.getenv('DDNS_ZONE')


def publicAddress():
    global currentIP
    print('Getting public IP from ifconfg.me...')

    r = requests.get('https://ifconfig.me')
    currentIP = r.text
    print('Public IP: {}'.format(currentIP))


def cloudflareDDNS():
    print('Checking IP recorded in Cloudflare...')
    ddnsRecord = getDDNSAddresszoneId(DDNS_ZONE)
    recordedIP = ddnsRecord['content']
    print('Found ddns recorded IP: {}'.format(recordedIP))

    if currentIP != recordedIP:
        print('Public IP has changed, updating all A records.')
        updateAllZones(recordedIP, currentIP)
    else:
        print('is same, exiting')


def main():
    apiKey = os.getenv('API_KEY')
    if apiKey is None:
        raise Exception('In .env file or environment set Cloudflare variable: API_KEY')
    if DDNS_ZONE is None:
        raise Exception('In .env file or environment; set Cloudflare zone where addr. points to current IP.')

    setAPIKey(apiKey)

    publicAddress()
    cloudflareDDNS()


if __name__ == '__main__':
    main()
