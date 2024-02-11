import os
import requests
from bulk_dns_update import updateAllZones, setAPIKey, getDDNSAddresszoneId
from notify import notify
from dotenv import load_dotenv
from logger import logger

load_dotenv()

currentIP = None
recordedIP = None
DDNS_ZONE = os.getenv('DDNS_ZONE')


def publicAddress():
    global currentIP
    logger.info('Getting public IP from ifconfg.me...')

    r = requests.get('https://ifconfig.me')
    currentIP = r.text
    logger.info('Public IP: {}'.format(currentIP))


def cloudflareDDNS():
    global recordedIP
    logger.info('Checking IP recorded in Cloudflare...')
    ddnsRecord = getDDNSAddresszoneId(DDNS_ZONE)
    recordedIP = ddnsRecord['content']
    logger.info('Found ddns recorded IP: {}'.format(recordedIP))

    if currentIP != recordedIP:
        logger.info('Public IP has changed, updating all A records.')
        return True
    else:
        logger.info('is same, exiting')
        return False


def main():
    apiKey = os.getenv('API_KEY')
    if apiKey is None:
        raise Exception('In .env file or environment set Cloudflare variable: API_KEY')
    if DDNS_ZONE is None:
        raise Exception('In .env file or environment; set Cloudflare zone where addr. points to current IP.')

    setAPIKey(apiKey)

    publicAddress()
    changed = cloudflareDDNS()

    if changed:
        notify("IP changed to: {}. Updating all cloudflare zones!".format(currentIP))
        updateAllZones(recordedIP, currentIP)


if __name__ == '__main__':
    main()
