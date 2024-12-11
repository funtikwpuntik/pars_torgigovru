from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils import data


# Универсальная функция для создания клавиатур
def create_keyboard(buttons: list[tuple[str, str]], row_width: int = 1, prev=None) -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for text, callback_data in buttons:  # Добавление кнопок
        builder.add(types.InlineKeyboardButton(text=text, callback_data=callback_data))
    if prev:  # Добавление кнопки "Назад", если указано
        builder.add(types.InlineKeyboardButton(text='Назад', callback_data=prev))

    builder.adjust(row_width)  # Установка ширины строк
    return builder.as_markup()


# Клавиатура фильтров
def filter_keyboard():
    return create_keyboard([
        ("Регион", "region"),  # Кнопка "Регион"
        ("Категория", "category"),  # Кнопка "Категория"
    ], 2, 'start')  # 2 кнопки в строке, кнопка "Назад" с callback 'start'


# Клавиатура категорий
def category_keyboard():
    return create_keyboard([
        ("Автомобили", "category?auto"),  # Кнопка "Автомобили"
        ("Недвижимость", "category?flat"),  # Кнопка "Недвижимость"
    ], 2, 'filter')  # 2 кнопки в строке, кнопка "Назад" с callback 'filter'


# Клавиатура регионов с постраничной навигацией
def region_keyboard(page=0):
    offset = page * 20  # Смещение для текущей страницы
    regions = list(data.subRF.items())[offset:offset + 20]  # Получение регионов для текущей страницы
    buttons = [(value['name'], f"region?{key}") for key, value in regions]  # Создание кнопок для регионов

    if offset > 0:  # Добавление кнопки "Назад" на предыдущую страницу
        buttons.append(("<<", "<<"))
    if offset + 20 < len(data.subRF):  # Добавление кнопки "Вперед" на следующую страницу
        buttons.append((">>", ">>"))

    return create_keyboard(buttons, 2, 'filter')  # 2 кнопки в строке, кнопка "Назад" с callback 'filter'


# Клавиатура управления лотами
def lot_keyboard(offset, count):
    buttons = [
        ('Анализ', 'analyze'),  # Кнопка "Анализ"
        ('Добавить в избранное', 'favorite'),  # Кнопка "Добавить в избранное"
        ('Назад', 'start'),  # Кнопка "Избранное"
        # ('Фильтр', 'filter'),  # Кнопка "Фильтр"
    ]
    if offset > 0:  # Добавление кнопки "Назад" по списку лотов
        buttons.append(("<<", "<<_lot"))
    if offset < count - 1:  # Добавление кнопки "Вперед" по списку лотов
        buttons.append((">>", ">>_lot"))
    return create_keyboard(buttons, 3)  # 4 кнопки в строке


# Клавиатура для управления избранным
def favorite_keyboard(offset, count):
    buttons = [
        #('Лоты', 'lots'),  # Кнопка "Лоты"
        ('Удалить из избранного', 'delete_favorite'),  # Кнопка "Удалить из избранного"
        ('Назад', 'start'),
    ]
    if offset > 0:  # Добавление кнопки "Назад" по списку избранного
        buttons.append(("<<", "<<_favorite"))
    if offset < count - 1:  # Добавление кнопки "Вперед" по списку избранного
        buttons.append((">>", ">>_favorite"))
    return create_keyboard(buttons, 2)  # 2 кнопки в строке, кнопка "Назад" с callback 'start'


# Пустая клавиатура (можно доработать под конкретные нужды)
def nd_keyboard():
    buttons = []
    return create_keyboard(buttons, prev='start')  # Пустая клавиатура, кнопка "Назад" с callback 'start'


# Клавиатура начального экрана
def start_keyboard():
    buttons = [
        ('Лоты', 'lots'),  # Кнопка "Лоты"
        ('Обновить все лоты', 'refresh_lots'),
        ('Избранное', 'look_favorite'),  # Кнопка "Избранное"
        ('Фильтр', 'filter'),  # Кнопка "Фильтр"
    ]
    return create_keyboard(buttons, 2)  # 3 кнопки в строке


# Клавиатура для администраторов
def admin_keyboard(users):
    buttons = [
        (f"{user['name']}\t{user['username']}", f"delete?{user['id']}") for user in users
        # Кнопки удаления пользователей
    ]
    return create_keyboard(buttons)  # Кнопки без дополнительного поведения
