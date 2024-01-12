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

    if data['success'] is False:
        print('Request to cloudflare was unsuccessful, error:')
        print(data['errors'])
        raise Exception('Unexpected Cloudflare error! Check logs.')

    if data['result'] is None or len(data['result']) < 1:
        # TODO
        print('no zones!')

    zones = list(map(lambda zone: getZoneInfo(zone), data['result']))
    return zones


def getRecordsForZone(zoneId):
    url = 'https://api.cloudflare.com/client/v4/zones/{}/dns_records?type=A'.format(zoneId)
    data = cloudflareRequest(url)

    if data['success'] is False:
        print('Request from cloudflare was unsuccessful, error:')
        print(data['errors'])
        raise Exception('Unexpected Cloudflare error! Check logs.')

    if data['result'] is None or len(data['result']) < 1:
        # TODO
        print('no records!')

    records = list(map(lambda record: getRecordInfo(record), data['result']))
    return records


def getDDNSAddresszoneId(ddnsZone):
    records = getRecordsForZone(ddnsZone)

    for record in records:
        if not re.match(r"^addr\.", record['name']):
            continue
        return record

    raise Exception('No ddns record found for zone: {}'.format(DDNS_ZONE))


def updateRecord(zoneId, recordId, name, newIP, ttl, proxied):
    url = 'https://api.cloudflare.com/client/v4/zones/{}/dns_records/{}'.format(zoneId, recordId)
    data = {
        'type': 'A',
        'name': name,
        'content': newIP,
        'ttl': ttl,
        'proxied': proxied
    }

    response = cloudflareUpdateRequest(url, data)
    print('\tRecord updated: {}'.format('✅' if response['success'] is True else '❌'))


def getMatchingRecordsForZone(zoneId, oldIP):
    records = getRecordsForZone(zoneId)
    return list(filter(lambda record: record['content'] == oldIP, records))


def updateZone(zone, oldIP, newIP):
    print('Updating records for {}'.format(zone['name']))
    records = getMatchingRecordsForZone(zone['id'], oldIP)
    if len(records) < 1:
        print('No matching records for {}\n'.format(zone['name']))
        return

    for record in records:
        print('\tRecord {}: {} -> {}'.format(record['name'], record['content'], newIP))
        updateRecord(zone['id'], record['id'], record['name'], newIP, record['ttl'], record['proxied'])

def updateAllZones(oldIP, newIP):
    zones = getZones()

    for zone in zones:
        updateZone(zone, oldIP, newIP)

if __name__ == '__main__':
    oldIP = input('Old IP address: ')
    newIP = input('New IP address: ')

    updateAllZones(oldIP, newIP)
