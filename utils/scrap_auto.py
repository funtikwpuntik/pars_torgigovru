from typing import Dict, List

import requests

from utils.data import headersAuto, cookiesAuto


# Получение ID геолокации города
def get_geo_id(city: str) -> int:
    """
    Получает geo_id для указанного города с сайта auto.ru.

    :param city: Название города
    :return: Geo ID города
    """
    json_data = {
        'letters': city,  # Вводим название города
        'geo_radius': 200,  # Радиус поиска
        'geo_id': [
            2,
        ],
    }
    response = requests.post(
        'https://auto.ru/-/ajax/desktop-search/getGeoSuggest/',
        cookies=cookiesAuto,  # cookies для авторизации
        headers=headersAuto,  # Заголовки запроса
        json=json_data  # Данные запроса
    ).json()[0]['id']
    return response  # Возвращаем geo_id


# Получение параметров поиска автомобилей
def get_parameters(geo: int, query: str, year: int) -> Dict:
    """
    Генерирует параметры для запроса поиска автомобиля.

    :param geo: Geo ID города
    :param query: Строка запроса (например, "Toyota Corolla")
    :param year: Год выпуска автомобиля
    :return: Словарь параметров для поиска
    """
    json_data = {
        'category': 'cars',  # Категория поиска: автомобили
        'query': query,  # Поисковый запрос
        'section': 'all',  # Поиск по всем секциям
        'geo_radius': 200,  # Радиус поиска
        'geo_id': [
            geo,  # Geo ID города
        ],
    }
    json_data = requests.post(
        'https://auto.ru/-/ajax/desktop-search/searchlineSuggest/',
        cookies=cookiesAuto,
        headers=headersAuto,
        json=json_data
    ).json()['suggests'][0]['params']

    # Дополнение параметров для поиска
    json_data.update({
        "year_from": year,  # Год выпуска
        "sort": "price-asc",  # Сортировка по цене (от меньшей к большей)
        "output_type": "list",  # Вывод в формате списка
        "geo_radius": 200,
        "geo_id": [
            geo
        ]
    })
    return json_data


# Получение данных об автомобиле
def get_data_auto(city: str, brand: str, model: str, year: int, sub_rf=None) -> List[str]:
    """
    Получает данные об автомобиле с auto.ru.

    :param city: Название города
    :param brand: Марка автомобиля
    :param model: Модель автомобиля
    :param year: Год выпуска автомобиля
    :param sub_rf: Регион (если город не указан)
    :return: Список с названием, ценой и ссылкой на автомобиль или сообщение об отсутствии данных
    """
    if sub_rf:  # Если указан регион, переопределяем город
        city = sub_rf
    geo = get_geo_id(city)  # Получаем geo_id города
    params = get_parameters(geo, f'{brand} {model}', year)  # Генерируем параметры поиска

    try:
        # Выполняем запрос к API auto.ru
        response = requests.post(
            'https://auto.ru/-/ajax/desktop-search/listing/',
            cookies=cookiesAuto,
            headers=headersAuto,
            json=params
        ).json()['offers'][0]  # Получаем первый найденный автомобиль

        # Формируем ответ с данными автомобиля
        ans = [response['title'], str(response['price_info']['RUR']), response['url']]
    except Exception as ex:  # Если возникает ошибка
        ans = ['Нет данных']  # Сообщение об отсутствии данных
    return ans
