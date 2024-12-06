import json
from typing import Dict

import requests

from data import params

cookies = {
    '_ym_uid': '1702801847394585950',
    '_ym_isad': '1',
    'gdpr': '0',
    '_ym_visorc': 'b',
    'spravka': 'dD0xNzMzNDgzMjMwO2k9NDYuMTM4LjI1Mi4zMTtEPTlFOUU5RUQzQTc1MzA4RTk1NDFDOEZCMDRCQTIxOTRBMjk4REI3Mjc2QkEzNEMyODYyMEM5NUY0RDM0Mjc0QjI2QUJEOUZFNzI1NDBEMUEwRjNFNTJCM0RDNDc2RjQwQURERDU5RUE3MkExM0NCNjk4NDM4RkE4QjlDM0FFMjdCRjg3MTk1MkE3MzEwNTNCQ0UyNTc4QTUyNDhBQzhBMDQzNjBFMjE2OTZDNTQzNDNDO3U9MTczMzQ4MzIzMDk2NjIxMjkyNTtoPTBlYjlmZDliZGQxYTIwYzFhNGViMWMwNTI2YWEzOGE4',
    'suid': 'dade58b5183d53737710f2a38d4a024b.824569c83f86fe2162a4388e1e4ebba9',
    '_csrf_token': '0275cea19dd583117022f7dad25545a52f439ef61feac4df',
    'autoruuid': 'g6752dadf22l18qleskaq8648qrmr8lu.79e3558c543aaddae81bf4de0f370121',
    'from': 'direct',
    'autoru_sso_blocked': '1',
    'Session_id': '3:1733483231.5.1.1686225980898:dnP8bQ:4b.1.2:1|1969619822.37500391.2.2:37500391.3:1723726371|255056641.-1.2.2:40891178.3:1727117158|61:10027906.960318.K4abaePgtp4_bsNB62_2Zm3jV8A',
    'sessar': '1.1196.CiBu5iEUMu-jWKIsu_01P41ivE910RTE_DoINJBGNyx9NA.80WN2Y8vBScdo7RGZk5JCW_DkKUShj7LcSltt47To54',
    'yandex_login': 'gorelovartem2000',
    'ys': 'udn.czoyNjg1ODg5NDp2azrQkNGA0YLQtdC80LjQuSDQk9C%2B0YDQtdC70L7Qsg%3D%3D#c_chck.1595445820',
    'i': 'w/7ss+hbg9p9fbRv03ohwYb/30JN0mwEOTglagptiD7llbIN6sE6IOlny4JgpkqXDKrdj1B3Buy48V5mZFBCECGjYts=',
    'yandexuid': '8169110051685964597',
    'my': 'YwA=',
    'L': 'eUlWSAtwb3MNBF9zaFcAd2EMeXpNT1d9BBskLBZdJyUlO1cAZ2VWdw==.1727117158.15897.335864.e1be3c78be10e5ebf3f89eb15b9c6565',
    'mda2_beacon': '1733483231292',
    'sso_status': 'sso.passport.yandex.ru:synchronized',
    'autoru_sso_redirect_blocked': '1',
    'crookie': 'zQYCVIfary7BDz7QWTdropsYizZVhsykzKLJ6tQvfpIMOInOcdztSQxBYIuFHPG3Z8wDdC2awkWFlSyohFOBxDH9k7c=',
    'cmtchd': 'MTczMzQ4MzIzNTM2MQ==',
    'fp': 'f682560858b7623e7a5bb6700fdc118c%7C1733483236239',
    'yaPassportTryAutologin': '1',
    'autoru_sid': '35130493%7C1733483235731.7776000.uuLzqZ-0ch6ze19BQUP8Nw.N_ZLOD_NSM8AR5LT2lPfyTw4zhGpmWxe54p9PHXvwsg',
    'los': '1',
    'bltsr': '1',
    'coockoos': '4',
    '_yasc': 'l1QCtacwPNvkvvHTNAOKiXUWqKfW3l7uS62Hqyls4mE3ArLOsodNL2krsnUItKgKUEq7N9Z4',
    'gids': '2',
    'gradius': '200',
    '_ym_d': '1733483433',
    'layout-config': '{"screen_height":1076,"screen_width":1640,"win_width":677,"win_height":950}',
    'count-visits': '3',
    'twins_popup': '1',
    'yaPlusUserPlusBalance': '{%22id%22:%2235130493%22%2C%22plusPoints%22:707}',
    'listing_view_session': '{}',
    'listing_view': '%7B%22output_type%22%3Anull%2C%22version%22%3A1%7D',
    'from_lifetime': '1733483565293',
}

headers = {
    'accept': '*/*',
    'accept-language': 'ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    # 'cookie': '_ym_uid=1702801847394585950; _ym_isad=1; gdpr=0; _ym_visorc=b; spravka=dD0xNzMzNDgzMjMwO2k9NDYuMTM4LjI1Mi4zMTtEPTlFOUU5RUQzQTc1MzA4RTk1NDFDOEZCMDRCQTIxOTRBMjk4REI3Mjc2QkEzNEMyODYyMEM5NUY0RDM0Mjc0QjI2QUJEOUZFNzI1NDBEMUEwRjNFNTJCM0RDNDc2RjQwQURERDU5RUE3MkExM0NCNjk4NDM4RkE4QjlDM0FFMjdCRjg3MTk1MkE3MzEwNTNCQ0UyNTc4QTUyNDhBQzhBMDQzNjBFMjE2OTZDNTQzNDNDO3U9MTczMzQ4MzIzMDk2NjIxMjkyNTtoPTBlYjlmZDliZGQxYTIwYzFhNGViMWMwNTI2YWEzOGE4; suid=dade58b5183d53737710f2a38d4a024b.824569c83f86fe2162a4388e1e4ebba9; _csrf_token=0275cea19dd583117022f7dad25545a52f439ef61feac4df; autoruuid=g6752dadf22l18qleskaq8648qrmr8lu.79e3558c543aaddae81bf4de0f370121; from=direct; autoru_sso_blocked=1; Session_id=3:1733483231.5.1.1686225980898:dnP8bQ:4b.1.2:1|1969619822.37500391.2.2:37500391.3:1723726371|255056641.-1.2.2:40891178.3:1727117158|61:10027906.960318.K4abaePgtp4_bsNB62_2Zm3jV8A; sessar=1.1196.CiBu5iEUMu-jWKIsu_01P41ivE910RTE_DoINJBGNyx9NA.80WN2Y8vBScdo7RGZk5JCW_DkKUShj7LcSltt47To54; yandex_login=gorelovartem2000; ys=udn.czoyNjg1ODg5NDp2azrQkNGA0YLQtdC80LjQuSDQk9C%2B0YDQtdC70L7Qsg%3D%3D#c_chck.1595445820; i=w/7ss+hbg9p9fbRv03ohwYb/30JN0mwEOTglagptiD7llbIN6sE6IOlny4JgpkqXDKrdj1B3Buy48V5mZFBCECGjYts=; yandexuid=8169110051685964597; my=YwA=; L=eUlWSAtwb3MNBF9zaFcAd2EMeXpNT1d9BBskLBZdJyUlO1cAZ2VWdw==.1727117158.15897.335864.e1be3c78be10e5ebf3f89eb15b9c6565; mda2_beacon=1733483231292; sso_status=sso.passport.yandex.ru:synchronized; autoru_sso_redirect_blocked=1; crookie=zQYCVIfary7BDz7QWTdropsYizZVhsykzKLJ6tQvfpIMOInOcdztSQxBYIuFHPG3Z8wDdC2awkWFlSyohFOBxDH9k7c=; cmtchd=MTczMzQ4MzIzNTM2MQ==; fp=f682560858b7623e7a5bb6700fdc118c%7C1733483236239; yaPassportTryAutologin=1; autoru_sid=35130493%7C1733483235731.7776000.uuLzqZ-0ch6ze19BQUP8Nw.N_ZLOD_NSM8AR5LT2lPfyTw4zhGpmWxe54p9PHXvwsg; los=1; bltsr=1; coockoos=4; _yasc=l1QCtacwPNvkvvHTNAOKiXUWqKfW3l7uS62Hqyls4mE3ArLOsodNL2krsnUItKgKUEq7N9Z4; gids=2; gradius=200; _ym_d=1733483433; layout-config={"screen_height":1076,"screen_width":1640,"win_width":677,"win_height":950}; count-visits=3; twins_popup=1; yaPlusUserPlusBalance={%22id%22:%2235130493%22%2C%22plusPoints%22:707}; listing_view_session={}; listing_view=%7B%22output_type%22%3Anull%2C%22version%22%3A1%7D; from_lifetime=1733483565293',
    'origin': 'https://auto.ru',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://auto.ru/sankt-peterburg/cars/kia/sportage/all/',
    'sec-ch-ua': '"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'same-origin',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0',
    'x-client-app-version': '277.0.15460111',
    'x-client-date': '1733483567010',
    'x-csrf-token': '0275cea19dd583117022f7dad25545a52f439ef61feac4df',
    'x-page-request-id': '5ae4a37383840de61aebe456950c63c7',
    'x-requested-with': 'XMLHttpRequest',
    'x-retpath-y': 'https://auto.ru/sankt-peterburg/cars/kia/sportage/all/',
    'x-yafp': '{"a1":"gcK8WQ==;0","a2":"W9GtWYG3V6hMBeN9EYmhpZfrpQYx6Q==;1","a3":"gw7t0+/IxivlxeOD9fAMLA==;2","a4":"/Q48NlSFXFZYjlMJthBwpK+lFtz6wCDi1jRBgZeCKkIFjg==;3","a5":"OxC6ZK5Fa7kN9w==;4","a6":"gRI=;5","a7":"g1XHSIbb8FTISA==;6","a8":"P3HX8NiPmaY=;7","a9":"92QP8kmvk1D9Ag==;8","b1":"xeGIVq+f85k=;9","b2":"9+8dSdatmtpZNQ==;10","b3":"ynFMEaJy38yKmA==;11","b4":"T1/dAecnO8I=;12","b5":"mUJnsGjhRSG7oA==;13","b6":"TzjyUErxJmXYmw==;14","b7":"7C0poLf/wy+vZw==;15","b8":"NczJ4Pw3dt3N7Q==;16","b9":"27y3r++96k656Q==;17","c1":"wCbMrw==;18","c2":"gp76iMC7O464vb1+p6q2l2o/;19","c3":"xxRVWy+0Ne972ox8/A9LOsI4;20","c4":"SrwlOTmrP/I=;21","c5":"bYNd2kjh8Ag=;22","c6":"JclqcQ==;23","c7":"vFL+/6Mj74U=;24","c8":"j8Y=;25","c9":"nsS2OCqKMDI=;26","d1":"4kuiAeJyR2Q=;27","d2":"qE+shQ==;28","d3":"m7/SGC6yrdIoIw==;29","d4":"63a1DvJ06Qk=;30","d5":"BoN6qs5/XSIgVg==;31","d7":"YKRpzRPF8Ss=;32","d8":"FzWHumq5nlB2taqwGfE+6jG5BQGVD79BDS8mUA==;33","d9":"GdtTElB5xxw=;34","e1":"xeiLbyny3HzdYQ==;35","e2":"n3JalW+HWmU=;36","e3":"AY20IojB6xc=;37","e4":"RVIv3xa+n/o=;38","e5":"ltG76QS8VnBJ5A==;39","e6":"awgYB02zsOg=;40","e7":"ilZf8z72jLNYFA==;41","e8":"wXfhjkexApg=;42","e9":"yhXCZ2W4o5Y=;43","f1":"xmsAeEb0DvN2dg==;44","f2":"NgVnoUqWwQA=;45","f3":"DFOlCmdBAFLMTg==;46","f4":"VF8IzgHIVvY=;47","f5":"/OzER8rQlZU/YA==;48","f6":"O9LD2X8NItwzhg==;49","f7":"NayCkxWkdSMXLQ==;50","f8":"RGsC5brmLVvhng==;51","f9":"piEgtMDhrJQ=;52","g1":"fEbKRs4PAaq9hA==;53","g2":"07A2A399Pc/mJg==;54","g3":"A7k0+rrJqlA=;55","g4":"OGinZGtgi0tGQg==;56","g5":"CVTo0c2/82c=;57","g6":"23U5lwRHKZY=;58","g7":"bywVqU75oPA=;59","g8":"Qfy88TMwlII=;60","g9":"1kcH8N1c34E=;61","h1":"QEfFJInoi3moTQ==;62","h2":"kjKYwl9puNZJOw==;63","h3":"n9c6TAj0Wto8vg==;64","h4":"oeeK+J/r0a9o4A==;65","h5":"rsq60OJ++R8=;66","h6":"39vugbcr8TvvfA==;67","h7":"2ZKFAOEMWC8VEXc7Z/UUFvTU1JNjVQoFmd4aWXxPjPrjoF9R;68","h8":"NORq1tZhvhRz/A==;69","h9":"UflMHesdiyxU0Q==;70","i1":"2yrKrNjlW58=;71","i2":"QhnKGaWaFd9MBg==;72","i3":"6VaeLv/WRgZ0cw==;73","i4":"prC+pIAw122tcA==;74","i5":"ZIVu5apcAcnUTw==;75","z1":"pkm6a4RsbKktwAF2LwRApQL74/itNbAdOfVX3SoBVupEeIYXnIek4aNG8EzesjGq6dR3MDkvg5bpUqedU2R4CA==;76","z2":"ODItlGbTRVlsZzd5QXUoTAUb55oB7gQbeXlZIAhgsOtiChufFpdh8lptmS38wa1wm5CMdk7tMTrepvV1LfXMdQ==;77","y2":"bUcSDE+vueHHNg==;78","y3":"szGRSCyD/R2ADw==;79","y6":"jSmtF9MqU4/aVg==;80","y8":"shJnENHx+8HkeQ==;81","x4":"HrvQPDF98hhZbw==;82","z4":"oecLr3iW+DtUHQ==;83","z5":"OHFHCuY34Fc=;84","z6":"5qAUXLgpsWNJICW2;85","z7":"84z9HBq36sMvvsIp;86","z8":"13djZusO3wjZNLzt;87","z9":"/M8W5fq6pvlml97b;88","y1":"OgEBTKGN2M6kW6PJ;89","y4":"RN13k5M1taEFMw/q;90","y5":"GHPern99fV9bMmZ94w8=;91","y7":"kw2FPhTLpwljmFrt;92","y9":"J97CQL0hCI/qtfgXFos=;93","y10":"1B6UjoAd8vgcUoP55EQ=;94","x1":"qscN1EvOmq3yaLOY;95","x2":"l472+dGvCE8oEe4aqY8=;96","x3":"/0WTUnTiN41Zu+Ac;97","x5":"yF+BYock4wCvpnFD;98","z3":"pvYZ2BmHTw6WDgIjBDxRz+XOuXXFTIAAAAIWL4b/3wk=;99","v":"6.3.1","pgrdt":"bNde75W4Nc72T5UBvdkEv1381KQ=;100","pgrd":"u8GJ/vCtpVIM2GTayRoCYwzEaza8FWxfBNon/kYUFTenLOMdAsML+O58nEesuQTBapbDB5MIn9K1VFp6ob5+Yg+kDLWl4w66uFuHuoIMVuWTzHXGs/J7FkXNm6T/wVVoqT4spEXBaEtyxbgEGh8meU5N0HYXq9+zXEp6LraCwpBRG1HC8BB1g/uBOYAOe3BkWHiqYBT9AcOqS96FPa0q3Aeyv1k="}',
}

def get_geo_id(city: str) -> int:
    json_data = {
        'letters': city,
        'geo_radius': 200,
        'geo_id': [
            2,
        ],
    }

    response = requests.post('https://auto.ru/-/ajax/desktop-search/getGeoSuggest/', cookies=cookies, headers=headers,
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
        cookies=cookies,
        headers=headers,
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
    response = requests.post('https://auto.ru/-/ajax/desktop-search/listing/', cookies=cookies, headers=headers, json=params).json()['offers']

    return response
# data_list = get_data_auto('Республика Адыгея', 'SKODA', 'SUPERB', 2014)
# with open('data.json', 'w', encoding='utf-8') as f:
#     f.write(json.dumps(data_list, indent=4))
# for i in data_list:
#     print(i['title'], i['url'], i['price_info']['RUR'])