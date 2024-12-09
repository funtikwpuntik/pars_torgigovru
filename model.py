from typing import List

from storage import LotsStorage, UsersStorage
from utils.scrap_torgi import get_data_from_torgi


# Функция для форматирования данных лота в текстовый вид
def get_text_data(lot):
    # Создает строку с подробной информацией о лоте
    text = (
        f"Описание: {lot['description']}\n"
        f"Местонахождение: {lot['region']}\n"
        f"Цена: {float(lot['price'])}\n"
        f"Окончание подачи заявок: {lot['date_end']}\n"
        f"Дата проведения торгов: {lot['auction_start']}\n"
        f"Электронная площадка: {lot['etpurl']}\n"
        f"Ссылка: {lot['link']}\n"
    )
    return text


# Класс для работы с лотами
class Lot:

    def __init__(self):
        self.lots = LotsStorage()  # Инициализация хранилища данных для лотов

    # Добавление новых лотов в хранилище
    def add_lots(self, region_id: int, category_code: int) -> List:
        # Получение данных о лотах с торговой площадки
        lots = get_data_from_torgi(region_id, category_code)

        # Форматирование данных о лотах для сохранения в хранилище
        data = [
            {
                "lot_id": lot['id'],
                "category_id": category_code,
                "description": lot['description'],
                "region": lot['city'] if lot['city'] else lot['sub_rf'],
                "region_id": region_id,
                "price": lot['priceMin'],
                "date_end": lot['endTime'],
                "auction_start": lot['auctionStart'],
                "etpurl": lot['etpurl'] if lot['etpurl'] else 'Нет',
                "link": lot['link']
            } for lot in lots
        ]

        # Формирование дополнительных данных о лотах в зависимости от категории
        if category_code == 9:  # Если категория — недвижимость
            data_info = [
                {
                    'flat_type': lot['type'],  # Тип недвижимости (например, квартира)
                    'square': lot['square'],  # Площадь недвижимости
                }
                for lot in lots
            ]
        if category_code == 100001:  # Если категория — автомобили
            data_info = [
                {
                    'brand': lot['brand'],  # Бренд автомобиля
                    'model': lot['model'],  # Модель автомобиля
                    'year': lot['year'],  # Год выпуска
                }
                for lot in lots
            ]

        # Добавление данных в хранилище
        return self.lots.add_data(data, data_info, category_code)

    # Получение лотов из хранилища по региону и категории
    def get_data_from_storage(self, region_id: int, category_id: int):
        lots = self.lots.get_data(region_id, category_id)
        return lots

    # Получение дополнительной информации о лоте недвижимости
    def info_flat(self, lot_id: int):
        return self.lots.get_info_flat(lot_id)

    # Получение дополнительной информации о лоте автомобиля
    def info_auto(self, lot_id: int):
        return self.lots.get_info_auto(lot_id)

    # Добавление лота в избранное
    def add_favorite(self, lot_id: int):
        return self.lots.add_favorite(lot_id)

    # Получение списка избранных лотов
    def get_favorites(self):
        self.lots.delete_non_actual_favorites()  # Удаление неактуальных избранных лотов
        return self.lots.get_favorites()

    # Удаление лота из избранного
    def delete_favorites(self, lot_id: int):
        return self.lots.delete_favorite(lot_id)


# Класс для работы с пользователями
class UsersModel:

    def __init__(self):
        self.users = UsersStorage()  # Инициализация хранилища данных для пользователей

    # Добавление нового пользователя в хранилище
    def add_user(self, message):
        data = {
            'telegram_id': message.chat.id,  # Идентификатор пользователя Telegram
            'name': message.chat.full_name,  # Полное имя пользователя
            'username': message.chat.username,  # Username пользователя
        }
        return self.users.add_user(data)

    # Получение списка всех пользователей
    def get_users(self):
        return self.users.get_users()

    # Удаление пользователя из хранилища
    def delete_user(self, user_id: int):
        return self.users.delete_user(user_id)
