from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils import data


def create_keyboard(buttons: list[tuple[str, str]], row_width: int = 1) -> types.InlineKeyboardMarkup:
    """
    Создаёт клавиатуру из списка кнопок.
    :param buttons: Список кортежей (текст, callback_data)
    :param row_width: Количество кнопок в строке
    :return: InlineKeyboardMarkup
    """
    builder = InlineKeyboardBuilder()
    for text, callback_data in buttons:
        builder.add(types.InlineKeyboardButton(text=text, callback_data=callback_data))
    builder.adjust(row_width)
    return builder.as_markup()


def filter_keyboard():
    return create_keyboard([("Регион", "region"), ("Категория", "category")], 2)


def category_keyboard():
    return create_keyboard([("Автомобили", "category?auto"), ("Недвижимость", "category?flat")], 2)


def region_keyboard(page=0):
    offset = page * 20
    regions = list(data.subRF.items())[offset:offset + 20]
    buttons = [(value['name'], f"region?{key}") for key, value in regions]

    if offset > 0:
        buttons.append(("<<", "<<"))
    if offset + 20 < len(data.subRF):
        buttons.append((">>", ">>"))

    return create_keyboard(buttons, row_width=2)


def lot_keyboard(offset, count):
    buttons = [('Анализ', 'analyze'), ('Добавить в избранное', 'favorite'),
               ('Избранное', 'look_favorite'), ('Фильтр', 'filter')]
    if offset > 0:
        buttons.append(("<<", "<<_lot"))
    if offset < count - 1:
        buttons.append((">>", ">>_lot"))
    return create_keyboard(buttons, 4)

def favorite_keyboard(offset, count):
    buttons = [('Лоты', 'lots'), ('Удалить из избранного', 'delete_favorite')]
    if offset > 0:
        buttons.append(("<<", "<<_favorite"))
    if offset < count - 1:
        buttons.append((">>", ">>_favorite"))
    return create_keyboard(buttons, 2)

def nd_keyboard():
    buttons = [('Лоты', 'lots'), ('Избранное', 'look_favorite')]
    return create_keyboard(buttons)

def start_keyboard():
    buttons = [('Лоты', 'lots'), ('Избранное', 'look_favorite'), ('Фильтр', 'filter')]
    return create_keyboard(buttons, 3)


def admin_keyboard(users):
    buttons = [
        (f"{user['name']}\t{user['username']}", f"delete?{user['id']}") for user in users
    ]
    return create_keyboard(buttons)