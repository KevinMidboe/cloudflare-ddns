import base64
import requests
from os import getenv
from json import dumps
from logger import logger


def notify(message):
    SMS_API_KEY = getenv('SMS_API_KEY')
    SMS_RECIPIENT = getenv('SMS_RECIPIENT')

    if not SMS_API_KEY:
        logger.info("No SMS API key found, not notifying")
        return

    if not SMS_RECIPIENT:
        logger.info("No SMS recipient found, not notifying")
        return

    recipient = "47{}".format(SMS_RECIPIENT)
    apiKey = base64.b64encode(SMS_API_KEY.encode("utf-8")).decode("utf-8")

    logger.info("Notifying of IP change over SMS")
    url = "https://gatewayapi.com/rest/mtsms"
    payload = {
        "sender": "Dynamic DNS",
        "message": message,
        "recipients": [{"msisdn": recipient}]
    }
    headers = {
        "Host": "gatewayapi.com",
        "Authorization": "Basic " + apiKey,
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    r = requests.post(url, data=dumps(payload), headers=headers)
    response = r.json()

    logger.info("Response from SMS api")
    logger.info("Status: {} {}".format(str(r.status_code), str(r.reason)))
    logger.info(response)
