from typing import Dict

import requests

from data import headersCian


# https://www.cian.ru/cian-api/site/v1/search-regions-cities/?text=Ярославль - aзш для поиска города


def get_json_data(square: float, region_id: int, lot_type: str) -> Dict:
    json_data = {
        'jsonQuery': {
            '_type': 'flatsale',
            'electronic_trading':{
                'type': 'term',
                'value': 2,
                },
            'engine_version':{
                'type': 'term',
                'value': 2,
                },
            'sort': {
                'type': 'term',
                'value': 'price_object_order',
                },
            'region': {
                'type': 'terms',
                'value': [region_id],
                },
            'total_area': {
                'type': 'range',
                'value': {
                    'gte': int(square)-5,
                    'lte': int(square)+5,
                },
            },
            'only_flat': {
                'type': 'term',
                'value': True,
            },
        },
    }
    if lot_type.lower() == 'комната':
        json_data['jsonQuery']['room'] = {
                'type': 'terms',
                'value': [0],
            }
    if lot_type.lower() == 'квартира':
        json_data['jsonQuery']['flat_share'] =  {
                'type': 'term',
                'value': 2,
            }
    else:
        json_data['jsonQuery']['flat_share'] = {
            'type': 'term',
            'value': 1,
        }
    return json_data


def get_region_id(city: str) -> int:
    response = requests.get(f'https://www.cian.ru/cian-api/site/v1/search-regions-cities/?text={city}').json()
    return response['data']['items'][0]['id']


def get_data_cian(type_lot: str, city: str, square: float, sub_rf=None):
    region_id = sub_rf if sub_rf else get_region_id(city)
    json_data = get_json_data(square, region_id, type_lot)
    response = requests.post(
        'https://api.cian.ru/search-offers/v2/search-offers-desktop/',
        # cookies=cookies,
        headers=headersCian,
        json=json_data,
    ).json()['data']['offersSerialized']
    try:
        text = [response[0]['formattedFullInfo'], str(response[0]['bargainTerms']['priceRur']), response[0]['fullUrl']]
    except Exception as ex:
        text = ['Нет данных']
    return text


# for i in get_data_cian('квартира', "москва", 31)[::-1]:
#     print(i)
#     print(i['fullUrl'], i['bargainTerms']['priceRur'])