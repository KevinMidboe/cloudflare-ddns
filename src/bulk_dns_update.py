#!/usr/bin/python3
'''
Cloudflare bulk DNS A record updater.

Designed to easily update all A records in cloudflare
from one IP to another. Usually after a new IP is
leased by ISP.

BEFORE RUNNING replace API_KEY with a key that holds
permission: DNS:Edit for one or more zones.
'''

import re
import requests
from logger import logger

API_KEY = ''


def setAPIKey(apiKey):
    global API_KEY
    API_KEY = apiKey


def cloudflareRequest(url):
    headers = {
        'Authorization': 'Bearer {}'.format(API_KEY),
        'Content-Type': 'application/json'
    }

    r = requests.get(url, headers=headers)
    return r.json()


def cloudflareUpdateRequest(url, data):
    headers = {
        'Authorization': 'Bearer {}'.format(API_KEY),
        'Content-Type': 'application/json'
    }

    r = requests.patch(url, headers=headers, json=data)
    return r.json()


def getZoneInfo(zone):
    return {
        'name': zone['name'],
        'id': zone['id']
    }


def getRecordInfo(record):
    return {
        'content': record['content'],
        'name': record['name'],
        'id': record['id'],
        'ttl': record['ttl'],
        'proxied': record['proxied']
    }


def getZones():
    url = 'https://api.cloudflare.com/client/v4/zones'
    data = cloudflareRequest(url)

    if 'success' not in data and 'errors' not in data:
        logger.info("Unexpected cloudflare error when getting zones, no response!")
        logger.info("data:" + str(data))
        raise Exception('Unexpected Cloudflare error, missing response! Check logs.')

    if data['success'] is False:
        logger.info('Request to cloudflare was unsuccessful, error:')
        logger.info(data['errors'])
        raise Exception('Unexpected Cloudflare error! Check logs.')

    if data['result'] is None or len(data['result']) < 1:
        # TODO
        logger.info('no zones!')

    zones = list(map(lambda zone: getZoneInfo(zone), data['result']))
    return zones


def getRecordsForZone(zoneId):
    url = 'https://api.cloudflare.com/client/v4/zones/{}/dns_records?type=A'.format(
        zoneId)
    data = cloudflareRequest(url)

    if 'success' not in data and 'errors' not in data:
        logger.info("Unexpected cloudflare error when getting records, no response!")
        logger.info("data:" + str(data))
        raise Exception('Unexpected Cloudflare error, missing response! Check logs.')

    if data['success'] is False:
        logger.info('Request from cloudflare was unsuccessful, error:')
        logger.info(data['errors'])
        raise Exception('Unexpected Cloudflare error! Check logs.')

    if data['result'] is None or len(data['result']) < 1:
        # TODO
        logger.info('no records!')

    records = list(map(lambda record: getRecordInfo(record), data['result']))
    return records


def getDDNSAddresszoneId(ddnsZone):
    records = getRecordsForZone(ddnsZone)

    for record in records:
        if not re.match(r"^addr\.", record['name']):
            continue
        return record

    raise Exception('No ddns record found for zone: {}'.format(ddnsZone))


def updateRecord(zoneId, recordId, name, newIP, ttl, proxied):
    url = 'https://api.cloudflare.com/client/v4/zones/{}/dns_records/{}'.format(
        zoneId, recordId)
    data = {
        'type': 'A',
        'name': name,
        'content': newIP,
        'ttl': ttl,
        'proxied': proxied
    }

    response = cloudflareUpdateRequest(url, data)
    logger.info('\tRecord updated: {}'.format(
        '✅' if response['success'] is True else '❌'))


def getMatchingRecordsForZone(zoneId, oldIP):
    records = getRecordsForZone(zoneId)
    return list(filter(lambda record: record['content'] == oldIP, records))


def updateZone(zone, oldIP, newIP):
    logger.info('Updating records for {}'.format(zone['name']))
    records = getMatchingRecordsForZone(zone['id'], oldIP)
    if len(records) < 1:
        logger.info('No matching records for {}\n'.format(zone['name']))
        return

    for record in records:
        logger.info(
            '\tRecord {}: {} -> {}'.format(record['name'], record['content'], newIP))
        updateRecord(zone['id'], record['id'], record['name'],
                     newIP, record['ttl'], record['proxied'])


def updateAllZones(oldIP, newIP):
    zones = getZones()

    for zone in zones:
        updateZone(zone, oldIP, newIP)


if __name__ == '__main__':
    oldIP = input('Old IP address: ')
    newIP = input('New IP address: ')

    updateAllZones(oldIP, newIP)
