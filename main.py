import os
import requests
from bulk_dns_update import updateAllZones, setAPIKey, getDDNSAddresszoneId
from dotenv import load_dotenv
from logger import logger

load_dotenv()

currentIP = None
DDNS_ZONE = os.getenv('DDNS_ZONE')


def publicAddress():
    global currentIP
    logger.info('Getting public IP from ifconfg.me...')

    r = requests.get('https://ifconfig.me')
    currentIP = r.text
    logger.info('Public IP: {}'.format(currentIP))


def cloudflareDDNS():
    logger.info('Checking IP recorded in Cloudflare...')
    ddnsRecord = getDDNSAddresszoneId(DDNS_ZONE)
    recordedIP = ddnsRecord['content']
    logger.info('Found ddns recorded IP: {}'.format(recordedIP))

    if currentIP != recordedIP:
        logger.info('Public IP has changed, updating all A records.')
        updateAllZones(recordedIP, currentIP)
    else:
        logger.info('is same, exiting')


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
