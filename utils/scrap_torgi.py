from typing import Dict, List
import data
import requests
from datetime import datetime, timedelta
import re

from data import subRF

def get_characteristics(characteristics_data: List) -> Dict:
    characteristics = {}
    for characteristic in characteristics_data:
        characteristics[characteristic['code']] = characteristic.get('characteristicValue', None)
    return characteristics

def get_city(address: str) -> str or None:

    city = re.search(r'г\.? (?:\w+\-?)+,?', address.replace('Респ', ''))
    if city:
        return ' '.join(city[0].replace(',', '').split()[1:])
    return None

def get_data_from_torgi(region: int, catcode: int) -> List:
    params = data.params
    if region:
        params['dynSubjRF'] = region
    params['catCode'] = catcode

    response = requests.get(
        'https://torgi.gov.ru/new/api/public/lotcards/search',
        # cookies=cookies,
        params=params,
        headers=data.headers,
    )
    lots = []
    for lot in response.json()['content']:
        lot_info = requests.get(f'https://torgi.gov.ru/new/api/public/lotcards/{lot["id"]}').json()
        hours = int(lot_info['timezoneOffset']) // 60
        date_end = datetime.strptime(lot_info['biddEndTime'], '%Y-%m-%dT%H:%M:%SZ') + timedelta(hours=hours)
        date_start = datetime.strptime(lot_info['auctionStartDate'], '%Y-%m-%dT%H:%M:%SZ') + timedelta(hours=hours)
        print(lot_info['estateAddress'])
        city = get_city(lot_info['estateAddress'])

        characteristics = get_characteristics(lot_info['characteristics'])
        lots.append(
            {
                'id': lot_info['id'],
                'description': lot_info['lotDescription'],
                'regionCode': lot_info['subjectRFCode'],
                'priceMin': lot_info['priceMin'],
                'endTime': date_end,
                'auctionStart': date_start,
                'etpurl': lot_info.get('etpUrl', None),
                'link': f'https://torgi.gov.ru/new/public/lots/lot/{lot_info["id"]}',
                'city': city,
                'sub_rf': None if city else subRF[lot_info['subjectRFCode']]['name'],
            }
        )
        if catcode == 9:
            lots[-1]['square'] = characteristics['totalAreaRealty']
            lots[-1]['type'] = characteristics['typeLivingQuarters']

        if catcode == 100001:
            year = re.search(r'[0-9]{4}', characteristics['yearProduction'])
            lots[-1]['year'] = int(year[0]) if year else None
            lots[-1]['brand'] = characteristics['carMarka']
            lots[-1]['model'] = characteristics['carModel']

            # lots[-1]['brand'] = lot_info['characteristics'][10]['characteristicValue']
            # lots[-1]['model'] = lot_info['characteristics'][11]['characteristicValue']




    return lots

