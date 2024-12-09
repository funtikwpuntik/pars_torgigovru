from typing import List

from utils.scrap_torgi import get_data_from_torgi
from storage import LotsStorage, UsersStorage


def get_text_data(lot):
    text = (
        f"Описание: {lot['description']}\n"
        f"Местонахождение: {lot['region']}\n"
        f"Цена: {float(lot['price'])}\n"
        f"Окончание подачи заявок: {lot['date_end']}\n"
        f"Дата проведения торгов: {lot['auction_start']}\n"
        f"Электронная площадка: {lot['etpurl']}\n"  # if lot['etpurl'] else 'Нет'
        f"Ссылка: {lot['link']}\n")

    return text


def get_data(region_id: int, category_code: int) -> List:
    lots = get_data_from_torgi(region_id, category_code)
    text = [
        (f"Описание: {lot['description']}\n"
         f"Местонахождение: {lot['city'] if lot['city'] else lot['sub_rf']}\n"
         f"Цена: {lot['priceMin']}\n"
         f"Окончание подачи заявок: {lot['endTime']}\n"
         f"Дата проведения торгов: {lot['auctionStart']}\n"
         f"Электронная площадка: {lot['etpurl'] if lot['etpurl'] else 'Нет'}\n"
         f"Ссылка: {lot['link']}\n") for lot in lots
    ]
    return text


class Lot:

    def __init__(self):
        self.lots = LotsStorage()


    # def get_offset_data(self, offset: int):

    def add_lots(self, region_id: int, category_code: int) -> List:
        lots = get_data_from_torgi(region_id, category_code)
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
                "link": lot['link']} for lot in lots
        ]
        if category_code == 9:
            data_info = [
                {
                    'flat_type': lot['type'],
                    'square': lot['square'],
                }
                for lot in lots
            ]
        if category_code == 100001:
            data_info = [
                {
                    'brand': lot['brand'],
                    'model': lot['model'],
                    'year': lot['year'],
                }
                for lot in lots
            ]
        return self.lots.add_data(data, data_info, category_code)

    def get_data_from_storage(self, region_id: int, category_id: int):
        lots = self.lots.get_data(region_id, category_id)
        return lots


    def info_flat(self, lot_id: int):
        return self.lots.get_info_flat(lot_id)

    def info_auto(self, lot_id: int):
        return self.lots.get_info_auto(lot_id)

    def add_favorite(self, lot_id: int):
        return self.lots.add_favorite(lot_id)

    def get_favorites(self):
        self.lots.delete_non_actual_favorites()
        return self.lots.get_favorites()

    def delete_favorites(self, lot_id: int):
        return self.lots.delete_favorite(lot_id)



class UsersModel:

    def __init__(self):
        self.users = UsersStorage()

    def add_user(self, message):
        data = {
            'telegram_id': message.chat.id,
            'name': message.chat.full_name,
            'username': message.chat.username,
        }
        return self.users.add_user(data)


    def get_users(self):
        return self.users.get_users()

    def delete_user(self, user_id: int):
        return self.users.delete_user(user_id)