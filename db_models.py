from datetime import datetime
from typing import List

from requests import session
from sqlalchemy import ForeignKey
from sqlalchemy import *
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import os

class Base(DeclarativeBase):
    pass

class Users(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(unique=True)
    name: Mapped[str] = mapped_column(String(64))
    username: Mapped[str] = mapped_column(String(32))

    def __repr__(self) -> str:
        return f"Users(id={self.telegram_id!r}, name={self.username!r})"

class Lots(Base):
    __tablename__ = "lots"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    lot_id: Mapped[str] = mapped_column(String, unique=True)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey('category.name_id'))
    description: Mapped[str] = mapped_column(String())
    region: Mapped[str] = mapped_column(String())
    region_id: Mapped[int] = mapped_column(Integer)
    price: Mapped[float] = mapped_column(DECIMAL)
    date_end: Mapped[datetime] = mapped_column(DATETIME)
    auction_start: Mapped[datetime] = mapped_column(DATETIME)
    etpurl: Mapped[str] = mapped_column(String(), nullable=True)
    link: Mapped[str] = mapped_column(String())

    # favorite: Mapped['Favorites'] = relationship(back_populates='lot')

class Category(Base):
    __tablename__ = 'category'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(64))
    name_id: Mapped[int] = mapped_column(Integer)

class Favorites(Base):
    __tablename__ = "favorites"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    lot_id: Mapped[int] = mapped_column(ForeignKey('lots.id'), unique=True)
    # lot: Mapped['Lots'] = relationship(back_populates='favorite')

class InfoLotFlat(Base):
    __tablename__ = "info_lot_flat"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    lot_id: Mapped[int] = mapped_column(ForeignKey('lots.id'), unique=True)
    square: Mapped[float] = mapped_column(DECIMAL)
    flat_type: Mapped[str] = mapped_column(String(16))




class InfoLotAuto(Base):
    __tablename__ = "info_lot_auto"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    lot_id: Mapped[int] = mapped_column(ForeignKey('lots.id'), unique=True)
    year: Mapped[int] = mapped_column(Integer, nullable=True)
    brand: Mapped[str] = mapped_column(String(), nullable=True)
    model: Mapped[str] = mapped_column(String(), nullable=True)





if not os.path.exists('lots.db'):
    engine = create_engine("sqlite+pysqlite:///lots.db", echo=True)
    Base.metadata.create_all(engine)
    session = engine.connect()
    session.execute(
        insert(Category), [
            {
                'name': 'Недвижимость',
                'name_id': 9,
            },
            {
                'name': 'Автомобиль',
                'name_id': 100001,
            },
        ]
    )
    session.commit()
    session.close()
