from typing import List, Dict

import sqlalchemy
from sqlalchemy import create_engine, select, insert, delete

from db_models import *


# Класс для работы с данными о лотах
class LotsStorage:

    def __init__(self):
        # Создание соединения с базой данных SQLite
        self.engine = create_engine("sqlite+pysqlite:///lots.db", echo=True)
        self.session = self.engine.connect()

    # Метод добавления данных о лотах в базу
    def add_data(self, data: List[Dict], data_info: List[Dict], category_id: int):
        # Определение таблицы в зависимости от категории
        table = InfoLotFlat if category_id == 9 else InfoLotAuto
        try:
            for index, value in enumerate(data):  # Итерация по списку данных о лотах
                # Вставка данных о лоте и получение его ID
                lot_id = self.session.execute(
                    insert(Lots).returning(Lots.id), value
                )
                lot_info = data_info[index]  # Получение дополнительной информации о лоте
                lot_info['lot_id'] = lot_id.scalars().all()[0]  # Связывание с ID лота
                # Вставка дополнительной информации в таблицу InfoLotFlat или InfoLotAuto
                self.session.execute(
                    insert(table), lot_info
                )
                self.session.commit()  # Сохранение изменений
        except sqlalchemy.exc.IntegrityError:
            self.session.commit()  # Обработка ошибок дублирования
            return '{ERROR: Lot already exist}'
        return '{success}'

    # Получение списка лотов по региону и категории
    def get_data(self, region_id: int, category_id: int):
        data = self.session.execute(
            select(
                Lots.id, Lots.description, Lots.region, Lots.price, Lots.date_end,
                Lots.auction_start, Lots.etpurl, Lots.link
            ).where(Lots.region_id == region_id, Lots.category_id == category_id)
            .order_by(Lots.id.desc())
        ).mappings().all()
        return data

    # Получение дополнительной информации о недвижимости
    def get_info_flat(self, lot_id: int):
        data = self.session.execute(
            select(InfoLotFlat).where(InfoLotFlat.lot_id == lot_id)
        ).mappings().all()
        return data

    # Получение дополнительной информации об автомобиле
    def get_info_auto(self, lot_id: int):
        data = self.session.execute(
            select(InfoLotAuto).where(InfoLotAuto.lot_id == lot_id)
        ).mappings().all()
        return data

    # Добавление лота в избранное
    def add_favorite(self, lot_id: int):
        try:
            self.session.execute(
                insert(Favorites), {'lot_id': lot_id}
            )
            self.session.commit()
        except sqlalchemy.exc.IntegrityError:
            return False
        return '{success}'

    # Получение списка избранных лотов
    def get_favorites(self):
        data = self.session.execute(
            select(
                Lots.id, Lots.description, Lots.region, Lots.price, Lots.date_end,
                Lots.auction_start, Lots.etpurl, Lots.link
            ).join(Favorites, Lots.id == Favorites.lot_id)
        ).mappings().all()
        return data

    # Удаление лота из избранного
    def delete_favorite(self, lot_id: int):
        self.session.execute(
            delete(Favorites).where(Favorites.lot_id == lot_id)
        )
        self.session.commit()
        return

    # Удаление неактуальных лотов из избранного
    def delete_non_actual_favorites(self):
        now = datetime.now()  # Текущее время
        subq = self.session.execute(
            select(Lots.id).where(Lots.date_end < now)
        ).scalars().all()  # Выборка неактуальных лотов
        self.session.execute(
            delete(Favorites).where(Favorites.lot_id.in_(subq))
        )
        self.session.commit()
        return

    # Закрытие соединения при удалении объекта
    def __del__(self):
        return self.session.close()


# Класс для работы с данными пользователей
class UsersStorage:

    def __init__(self):
        # Создание соединения с базой данных SQLite
        self.engine = create_engine("sqlite+pysqlite:///lots.db", echo=True)
        self.session = self.engine.connect()

    # Добавление нового пользователя в базу данных
    def add_user(self, data: Dict):
        try:
            self.session.execute(
                insert(Users), data
            )
        except sqlalchemy.exc.IntegrityError:
            return '{ERROR: User already exist}'
        self.session.commit()

    # Получение списка пользователей
    def get_users(self):
        data = self.session.execute(
            select(Users.id, Users.name, Users.username)
        ).mappings().all()
        return data

    # Удаление пользователя из базы
    def delete_user(self, user_id: int):
        self.session.execute(
            delete(Users).where(Users.id == user_id)
        )
        self.session.commit()
        return

    # Закрытие соединения при удалении объекта
    def __del__(self):
        return self.session.close()
