from typing import Dict, List

import requests

from utils.data import headersCian  # Импорт заголовков для запросов


# Генерация данных для JSON-запроса
def get_json_data(square: float, region_id: int, lot_type: str) -> Dict:
    """
    Формирует JSON-данные для запроса на поиск объектов недвижимости.

    :param square: Площадь объекта (в м²)
    :param region_id: ID региона
    :param lot_type: Тип объекта ("квартира" или "комната")
    :return: Словарь с JSON-данными для запроса
    """
    json_data = {
        'jsonQuery': {
            '_type': 'flatsale',  # Тип сделки: продажа квартир
            'electronic_trading': {
                'type': 'term',
                'value': 2,  # Электронные торги
            },
            'engine_version': {
                'type': 'term',
                'value': 2,  # Версия движка поиска
            },
            'sort': {
                'type': 'term',
                'value': 'price_object_order',  # Сортировка по цене
            },
            'region': {
                'type': 'terms',
                'value': [region_id],  # ID региона
            },
            'total_area': {
                'type': 'range',
                'value': {
                    'gte': int(square) - 5,  # Нижняя граница площади
                    'lte': int(square) + 5,  # Верхняя граница площади
                },
            },
            'only_flat': {
                'type': 'term',
                'value': True,  # Исключить нежилые помещения
            },
        },
    }

    # Настройки по типу объекта
    if lot_type.lower() == 'комната':
        json_data['jsonQuery']['room'] = {
            'type': 'terms',
            'value': [0],  # Комнаты
        }
    elif lot_type.lower() == 'квартира':
        json_data['jsonQuery']['flat_share'] = {
            'type': 'term',
            'value': 2,  # Полностью квартира
        }
    else:
        json_data['jsonQuery']['flat_share'] = {
            'type': 'term',
            'value': 1,  # Доля в квартире
        }

    return json_data


# Получение ID региона по названию города
def get_region_id(city: str) -> int:
    """
    Получает ID региона для указанного города с API Cian.

    :param city: Название города
    :return: ID региона
    """
    response = requests.get(
        f'https://www.cian.ru/cian-api/site/v1/search-regions-cities/?text={city}'
    ).json()
    return response['data']['items'][0]['id']  # ID первого найденного региона


# Получение данных по объектам недвижимости
def get_data_cian(type_lot: str, city: str, square: float, sub_rf=None) -> List[str]:
    """
    Получает данные об объекте недвижимости с Cian.

    :param type_lot: Тип объекта ("квартира" или "комната")
    :param city: Название города
    :param square: Площадь объекта
    :param sub_rf: ID региона (если указан)
    :return: Список с названием, ценой, и ссылкой на объект или сообщение об отсутствии данных
    """
    region_id = sub_rf if sub_rf else get_region_id(city)  # Получаем ID региона
    json_data = get_json_data(square, region_id, type_lot)  # Формируем данные запроса

    try:
        response = requests.post(
            'https://api.cian.ru/search-offers/v2/search-offers-desktop/',
            headers=headersCian,  # Заголовки запроса
            json=json_data  # Данные запроса
        ).json()['data']['offersSerialized']  # Извлекаем предложения

        # Формируем ответ с данными объекта
        text = [
            response[0]['formattedFullInfo'],  # Полное описание
            str(response[0]['bargainTerms']['priceRur']),  # Цена
            response[0]['fullUrl'],  # Ссылка на объект
        ]
    except Exception as ex:  # Обработка ошибок
        text = ['Нет данных']  # Сообщение об отсутствии данных

    return text
