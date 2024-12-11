import re
from datetime import datetime, timedelta
from typing import Dict, List

import requests

from utils import data


def get_session():
    session = requests.Session()
    session.headers.update(data.headers)
    return session

# Функция для извлечения характеристик из данных
def get_characteristics(characteristics_data: List) -> Dict:
    characteristics = {}
    for characteristic in characteristics_data:  # Итерация по списку характеристик
        characteristics[characteristic['code']] = characteristic.get('characteristicValue', None)
    return characteristics  # Возврат словаря характеристик


# Функция для извлечения города из адреса
def get_city(address: str) -> str or None:
    city = re.search(r'г\.? (?:\w+\-?)+,?', address.replace('Респ', ''))  # Поиск названия города
    if city:
        return ' '.join(city[0].replace(',', '').split()[1:])  # Удаление лишних символов и возврат города
    return None  # Если город не найден, вернуть None


# Функция для получения данных с портала torgi.gov.ru
def get_data_from_torgi(region: int, catcode: int, page=None) -> List:
    params = data.params  # Основные параметры запроса
    if region:  # Если регион указан, добавить его в параметры
        params['dynSubjRF'] = region
    params['catCode'] = catcode  # Добавление кода категории
    if page:
        params['withFacets'] = False
        params['page'] = page
    # Выполнение запроса для поиска лотов
    session = get_session()

    response = session.get(
        'https://torgi.gov.ru/new/api/public/lotcards/search',
        params=params,  # Параметры запроса
        headers=data.headers,  # Заголовки запроса
    )
    lots = []  # Список для сохранения информации о лотах

    # Итерация по полученным данным
    for lot in response.json()['content']:
        # Запрос для получения полной информации о конкретном лоте
        lot_info = session.get(f'https://torgi.gov.ru/new/api/public/lotcards/{lot["id"]}').json()
        hours = int(lot_info['timezoneOffset']) // 60  # Часовой пояс
        # Конвертация дат с учетом часового пояса
        date_end = datetime.strptime(lot_info['biddEndTime'], '%Y-%m-%dT%H:%M:%SZ') + timedelta(hours=hours)
        date_start = datetime.strptime(lot_info['auctionStartDate'], '%Y-%m-%dT%H:%M:%SZ') + timedelta(hours=hours)
        city = get_city(lot_info['estateAddress'])  # Получение города из адреса

        characteristics = get_characteristics(lot_info['characteristics'])  # Получение характеристик лота
        # Формирование записи для списка лотов
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
                'sub_rf': None if city else data.subRF[lot_info['subjectRFCode']]['name'],  # Определение региона
            }
        )
        # Обработка данных для категории "Недвижимость" (catcode == 9)
        if catcode == 9:
            lots[-1]['square'] = characteristics['totalAreaRealty']  # Площадь объекте
            type_flat = characteristics['typeLivingQuarters'].lower()  # Тип объекта
            if type_flat == 'комната' or type_flat == 'квартира':
                lots[-1]['type'] = type_flat
            elif type_flat == 'жилое' and 'доля' not in lot_info['lotDescription'].lower():
                lots[-1]['type'] = 'квартира'
            elif type_flat == 'доля' or 'доля' in lot_info['lotDescription'].lower():
                lots[-1]['type'] = 'доля'
            else:
                lots[-1]['type'] = 'квартира'
        # Обработка данных для категории "Автомобили" (catcode == 100001)
        if catcode == 100001:
            if lot_info['lotName'] not in lot_info['lotDescription'] and lot_info.get('lotName', None):
                # Если название отсутствует в описании, добавляем его
                lots[-1]['description'] = lot_info['lotName'] + ' ' + lots[-1]['description']
            # Извлечение года выпуска из данных
            year = re.search(r'[0-9]{4}', characteristics['yearProduction'])
            lots[-1]['year'] = int(year[0]) if year else None
            lots[-1]['brand'] = characteristics['carMarka']  # Марка автомобиля
            lots[-1]['model'] = characteristics['carModel']  # Модель автомобиля
    session.close()
    return lots  # Возврат списка лотов

def get_pages(region: int, catcode: int):
    params = data.params  # Основные параметры запроса
    if region:  # Если регион указан, добавить его в параметры
        params['dynSubjRF'] = region
    params['catCode'] = catcode  # Добавление кода категории

    # Выполнение запроса для поиска лотов
    response = requests.get(
        'https://torgi.gov.ru/new/api/public/lotcards/search',
        params=params,  # Параметры запроса
        headers=data.headers,  # Заголовки запроса
    )
    return response.json()['totalPages']