from typing import Dict, List
import data
import requests
from datetime import datetime, timedelta


def get_data_from_torgi(region: int, catcode: int) -> List:
    params = data.params
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
        lot_info = requests.get(f'https://torgi.gov.ru/new/api/public/lotcards/{lot["id"]}').json(decode='utf-8')
        hours = int(lot_info['timezoneOffset']) // 60
        date_end = datetime.strptime(lot_info['biddEndTime'], '%Y-%m-%dT%H:%M:%SZ') + timedelta(hours=hours)
        date_start = datetime.strptime(lot_info['auctionStartDate'], '%Y-%m-%dT%H:%M:%SZ')
        lots.append(
            {
                'id': lot_info['id'],
                'description': lot_info['lotDescription'],
                'regionCode': lot_info['subjectRFCode'],
                'priceMin': lot_info['priceMin'],
                'endTime': date_end,
                'auctionStart': date_start,
                'etpurl': lot_info['etpUrl'],
                'link': f'https://torgi.gov.ru/new/public/lots/lot/{lot_info["id"]}',
            }
        )

    return lots
