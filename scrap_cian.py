from typing import Dict

import requests

headers = {
    'accept': '*/*',
    'accept-language': 'ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    # 'cookie': '_CIAN_GK=46760bf7-8c6f-4bde-9927-20fa2be01a18; __cf_bm=SGiX8RjE.7mZguSHUCsJ4Fy74t1SKLJGooXaXJeuYFE-1733234667-1.0.1.1-oDG6w7ezIdNo9DkfLKvg_UxmravZxt18XCtCZaWM_KoWWdcQqJECE7IAGxEUNp.7gOAF.s2lY0wdiPuzSXfs5g; cat_profiling=1; cf_clearance=dO6MM67ZqFjbhoXGC8n1pv_ZCQiy78EbWg9wfsmtST4-1733234669-1.2.1.1-E5NfQvTZXrCZQH4hZAjEvUnxxGV2ieji4C1wNTcVGbQcFswy4YQ1SGTN3.m.jg6wl6zlkHGle5zBA7WSGi.glFw916hVypH9UrIijZCTW94sCGToUbBmGxXpPlvzZZpHV9wfrFGJK8_hNGMOZ6wqBQp03b2PK2qem9DUFEvpihkx29n__LVRyLcwOpUk610ucfP_5a740_PvV2AGM4C3GGRD_olPCDv2ICvg2rNn5W7dX8USTfw6U7QwVr5AlcY.K6btzT6.H9ysZCQoo3F4oDJcZONZlpLMGOOhWnuz2GhzSR0BJpk4p.xIdwT757i5gFPNxDjEzwe5MuRdRORh5fXvJzCnN.b96tJ_aPrFLHHucilB4g.SIZAJLAQVaAaXeTbjP0D3vqtspPPWqcJrJQ; _gcl_au=1.1.1599919042.1733234669; login_mro_popup=1; sopr_utm=%7B%22utm_source%22%3A+%22google%22%2C+%22utm_medium%22%3A+%22organic%22%7D; uxfb_usertype=searcher; _ga=GA1.1.1673024529.1733234671; sopr_session=3bd388ea3cb74854; _ym_uid=1691686469369136487; _ym_d=1733234672; _ym_isad=1; _ym_visorc=b; uxs_uid=84c6d1c0-b17f-11ef-8717-d5b1d34578d1; login_button_tooltip_key=1; afUserId=e8307ae6-4a9b-40ef-9c2b-d7be3608a3b6-p; AF_SYNC=1733234673199; cookie_agreement_accepted=1; session_region_id=174292; session_main_town_region_id=174292; _ga_3369S417EL=GS1.1.1733234671.1.1.1733234810.57.0.0',
    'origin': 'https://cian.ru',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://cian.ru/',
    'sec-ch-ua': '"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0',
}
# https://www.cian.ru/cian-api/site/v1/search-regions-cities/?text=Ярославль - aзш для поиска города


def get_json_data(square: float, region_id: int, lot_type: str) -> Dict:
    json_data = {
        'jsonQuery': {
            '_type': 'flatsale',
            'electronic_trading':{
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
            'flat_share': {
                'type': 'term',
                'value': 2 if lot_type.lower() == 'квартира' else 1,
            },
        },
    }

    return json_data


def get_region_id(city: str) -> int:
    response = requests.get(f'https://www.cian.ru/cian-api/site/v1/search-regions-cities/?text={city}').json()
    return response['data']['items'][0]['id']


def get_data_cian(type_lot: str, city: str, square: float):
    region_id = get_region_id(city)
    json_data = get_json_data(square, region_id, type_lot)
    response = requests.post(
        'https://api.cian.ru/search-offers/v2/search-offers-desktop/',
        # cookies=cookies,
        headers=headers,
        json=json_data,
    ).json()['data']['offersSerialized'][0]['bargainTerms']['priceRur']

    return response

