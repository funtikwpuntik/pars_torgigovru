from typing import Dict

import requests

from data import headersAuto, cookiesAuto

def get_geo_id(city: str) -> int:
    json_data = {
        'letters': city,
        'geo_radius': 200,
        'geo_id': [
            2,
        ],
    }

    response = requests.post('https://auto.ru/-/ajax/desktop-search/getGeoSuggest/', cookies=cookiesAuto, headers=headersAuto,
                             json=json_data).json()[0]['id']
    return response


def get_parameters(geo: int, query: str, year: int) -> Dict:
    json_data = {
        'category': 'cars',
        'query': query,
        'section': 'all',
        'geo_radius': 200,
        'geo_id': [
            geo,
        ],
    }
    json_data = requests.post(
        'https://auto.ru/-/ajax/desktop-search/searchlineSuggest/',
        cookies=cookiesAuto,
        headers=headersAuto,
        json=json_data,
    ).json()['suggests'][0]['params']

    json_data.update({
      "year_from": year,
      "sort": "price-asc",
      "output_type": "list",
      "geo_radius": 200,
      "geo_id": [
          geo
      ]
    })
    return json_data

def get_data_auto(city: str, brand: str, model: str, year: int, sub_rf=None):
    if sub_rf:
        city = sub_rf
    geo = get_geo_id(city)
    params = get_parameters(geo, f'{brand} {model}', year)
    try:
        response = requests.post('https://auto.ru/-/ajax/desktop-search/listing/', cookies=cookiesAuto, headers=headersAuto, json=params).json()['offers'][0]
        ans = [response['title'], str(response['price_info']['RUR']), response['url']]
    except Exception as ex:
        ans = ['Нет данных']
    return ans
