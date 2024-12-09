import os
from datetime import datetime

from sqlalchemy import *
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column


# Базовый класс для декларативного описания моделей
class Base(DeclarativeBase):
    pass


# Модель для таблицы пользователей
class Users(Base):
    __tablename__ = "users"  # Название таблицы в базе данных
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)  # Первичный ключ с автоинкрементом
    telegram_id: Mapped[int] = mapped_column(unique=True)  # Уникальный идентификатор Telegram
    name: Mapped[str] = mapped_column(String(64))  # Имя пользователя (до 64 символов)
    username: Mapped[str] = mapped_column(String(32))  # Username (до 32 символов)

    def __repr__(self) -> str:
        # Строковое представление объекта
        return f"Users(id={self.telegram_id!r}, name={self.username!r})"


# Модель для таблицы лотов
class Lots(Base):
    __tablename__ = "lots"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)  # Первичный ключ
    lot_id: Mapped[str] = mapped_column(String, unique=True)  # Уникальный идентификатор лота
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey('category.name_id'))  # Внешний ключ на категорию
    description: Mapped[str] = mapped_column(String())  # Описание лота
    region: Mapped[str] = mapped_column(String())  # Название региона
    region_id: Mapped[int] = mapped_column(Integer)  # Идентификатор региона
    price: Mapped[float] = mapped_column(DECIMAL)  # Цена лота
    date_end: Mapped[datetime] = mapped_column(DATETIME)  # Дата окончания аукциона
    auction_start: Mapped[datetime] = mapped_column(DATETIME)  # Дата начала аукциона
    etpurl: Mapped[str] = mapped_column(String(), nullable=True)  # URL электронных торгов (опционально)
    link: Mapped[str] = mapped_column(String())  # Ссылка на лот


# Модель для таблицы категорий
class Category(Base):
    __tablename__ = 'category'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)  # Первичный ключ
    name: Mapped[str] = mapped_column(String(64))  # Название категории (например, "Недвижимость")
    name_id: Mapped[int] = mapped_column(Integer)  # Идентификатор категории (например, 9 для недвижимости)


# Модель для таблицы избранных лотов
class Favorites(Base):
    __tablename__ = "favorites"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)  # Первичный ключ
    lot_id: Mapped[int] = mapped_column(ForeignKey('lots.id'), unique=True)  # Внешний ключ на таблицу лотов


# Модель для информации о лотах недвижимости
class InfoLotFlat(Base):
    __tablename__ = "info_lot_flat"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)  # Первичный ключ
    lot_id: Mapped[int] = mapped_column(ForeignKey('lots.id'), unique=True)  # Внешний ключ на таблицу лотов
    square: Mapped[float] = mapped_column(DECIMAL)  # Площадь объекта
    flat_type: Mapped[str] = mapped_column(String(16))  # Тип недвижимости (например, квартира или дом)


# Модель для информации о лотах автомобилей
class InfoLotAuto(Base):
    __tablename__ = "info_lot_auto"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)  # Первичный ключ
    lot_id: Mapped[int] = mapped_column(ForeignKey('lots.id'), unique=True)  # Внешний ключ на таблицу лотов
    year: Mapped[int] = mapped_column(Integer, nullable=True)  # Год выпуска автомобиля
    brand: Mapped[str] = mapped_column(String(), nullable=True)  # Бренд автомобиля
    model: Mapped[str] = mapped_column(String(), nullable=True)  # Модель автомобиля


# Проверка наличия файла базы данных
if not os.path.exists('lots.db'):
    engine = create_engine("sqlite+pysqlite:///lots.db", echo=True)  # Создание подключения к SQLite
    Base.metadata.create_all(engine)  # Создание всех таблиц, если их нет
    session = engine.connect()  # Установка соединения с базой
    # Добавление категорий "Недвижимость" и "Автомобиль" в таблицу категорий
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
    session.commit()  # Фиксация изменений
    session.close()  # Закрытие соединения
