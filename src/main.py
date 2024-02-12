import os
import re
import requests
from bulk_dns_update import updateAllZones, setAPIKey, getDDNSAddresszoneId
from notify import notify
from dotenv import load_dotenv
from logger import logger

load_dotenv()

DDNS_ZONE = os.getenv('DDNS_ZONE')


def validIP(ipString):
    ipRegex = '^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$'
    return bool(re.search(ipRegex, str(ipString)))


def publicAddress():
    logger.info('Getting public IP from ifconfg.me...')

    r = requests.get('https://ifconfig.me')
    if r.status_code != 200:
        return

    ip = r.text
    if not validIP(ip):
        return

    logger.info('Public IP: {}'.format(ip))
    return ip


def cloudflareDDNS():
    logger.info('Checking IP recorded in Cloudflare...')
    ddnsRecord = getDDNSAddresszoneId(DDNS_ZONE)
    ip = ddnsRecord['content']
    logger.info('Found ddns recorded IP: {}'.format(ip))

    if not validIP(ip):
        return

    return ip


def main():
    apiKey = os.getenv('API_KEY')
    if apiKey is None:
        raise Exception(
            'In .env file or environment set Cloudflare variable: API_KEY')
    if DDNS_ZONE is None:
        raise Exception(
            'In .env file or environment; set Cloudflare zone where addr. points to current IP.')

    setAPIKey(apiKey)

    currentIP = publicAddress()
    recordedIP = cloudflareDDNS()

    if currentIP == recordedIP or None in [currentIP, recordedIP]:
        logger.info('is same, exiting')
        return

    logger.info('Public IP has changed, updating all A records.')
    notify("IP changed to: {}. Updating all cloudflare zones!".format(currentIP))
    updateAllZones(recordedIP, currentIP)


if __name__ == '__main__':
    main()
