from pydantic.v1 import DictError

from db_models import *
import json
from typing import List, Dict

import sqlalchemy
from sqlalchemy import create_engine, select, update, insert, bindparam, or_


class LotsStorage:

    def __init__(self):
        self.engine = create_engine("sqlite+pysqlite:///lots.db", echo=True)
        self.session = self.engine.connect()

    def add_data(self, data: List[Dict], data_info: List[Dict], category_id: int):
        table = InfoLotFlat if category_id == 9 else InfoLotAuto
        try:
            for index, value in enumerate(data):
                lot_id = self.session.execute(
                insert(Lots).returning(Lots.id), value)
                lot_info = data_info[index]
                lot_info['lot_id'] = lot_id.scalars().all()[0]
                self.session.execute(
                    insert(table), data_info[index]
                )
                self.session.commit()
        except sqlalchemy.exc.IntegrityError:
            return '{ERROR: Lot already exist}'
        return '{success}'

    def get_data(self, region_id: int, category_id: int):
        data = self.session.execute(
            select(
            Lots.id, Lots.description, Lots.region, Lots.price, Lots.date_end, Lots.auction_start, Lots.etpurl, Lots.link
        ).where(Lots.region_id == region_id, Lots.category_id == category_id).order_by(Lots.id.desc())).mappings().all()
        return data

    def get_info_flat(self, lot_id: int):
        data = self.session.execute(
            select(
                InfoLotFlat
            ).where(InfoLotFlat.lot_id == lot_id)
        ).mappings().all()
        return data

    def get_info_auto(self, lot_id: int):
        data = self.session.execute(
            select(
                InfoLotAuto
            ).where(InfoLotAuto.lot_id == lot_id)
        ).mappings().all()
        return data

    def add_favorite(self, lot_id: int):
        try:
            self.session.execute(
                insert(Favorites), {'lot_id': lot_id}
            )
            self.session.commit()
        except sqlalchemy.exc.IntegrityError:
            return False
        return '{success}'

    def get_favorites(self):
        data = self.session.execute(
            select(
                Lots.id, Lots.description, Lots.region, Lots.price, Lots.date_end, Lots.auction_start, Lots.etpurl,
                Lots.link
            ).join(Favorites, Lots.id == Favorites.lot_id)).mappings().all()
        return data

    def delete_favorite(self, lot_id: int):
        self.session.execute(delete(Favorites).where(Favorites.lot_id == lot_id))
        self.session.commit()
        return

    def delete_non_actual_favorites(self):
        now = datetime.now()
        subq = self.session.execute(select(Lots.id).where(Lots.date_end < now))
        self.session.execute(
            delete(Favorites).where(Favorites.lot_id.in_(subq))
        )
        self.session.commit()
        return

    def __del__(self):
        return self.session.close()


class UsersStorage:

    def __init__(self):
        self.engine = create_engine("sqlite+pysqlite:///lots.db", echo=True)
        self.session = self.engine.connect()

    def add_user(self, data: Dict):
        try:
            self.session.execute(
                insert(Users), data)
        except sqlalchemy.exc.IntegrityError:

            return '{ERROR: User already exist}'

        self.session.commit()

    def get_users(self):
        data = self.session.execute(
            select(
                Users.id, Users.name, Users.username,
            )).mappings().all()
        return data

    def delete_user(self, user_id: int):
        self.session.execute(delete(Users).where(Users.id == user_id))
        self.session.commit()
        return

    def __del__(self):
        return self.session.close()