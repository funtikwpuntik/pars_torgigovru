from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from model import Lot, get_text_data, UsersModel
from utils.keyboards import *
from utils.scrap_auto import get_data_auto
from utils.scrap_cian import get_data_cian
from utils.scrap_torgi import get_pages


# Определение группы состояний для управления фильтром лотов
class LotsFilter(StatesGroup):
    region = State()  # Состояние выбора региона
    category = State()  # Состояние выбора категории
    lots = State()  # Состояние просмотра лотов


# Стандартные значения, используемые при старте
default_values = {
    'region': 78,  # Код региона по умолчанию
    'category': 9,  # Код категории по умолчанию
    'offset': 0,  # Смещение для пагинации
    'lot_offset': 0,  # Текущее смещение лота
    'count': 0,  # Количество доступных лотов
    'lots': [],  # Список лотов
}

router = Router()  # Создание роутера для управления обработчиками


# Функция для добавления лота в избранное, если его цена соответствует условиям
def add_favorite(lot_price, price, lot_id):
    if float(lot_price) * 1.35744 <= float(price):  # Проверка цены
        Lot().add_favorite(lot_id)  # Добавление в избранное
        return '\nДобавлено в избранное\n'
    return ''


# Универсальная функция для обработки кнопок "вперед" и "назад" в пагинации
async def navigate(callback: types.CallbackQuery, state: FSMContext, key: str, direction: int, keyboard_fn):
    state_data = await state.get_data()  # Получение текущих данных состояния
    offset = state_data[key] + direction  # Обновление смещения
    await state.update_data({key: offset})  # Сохранение нового смещения
    lot = state_data['lots'][offset]  # Получение текущего лота
    text = get_text_data(lot)  # Формирование текста для отображения
    await callback.message.edit_text(text,
                                     reply_markup=keyboard_fn(offset, state_data['count']))  # Обновление сообщения


# Обработчик команды /start
@router.message(Command("start"))
async def start(message: Message, state: FSMContext):
    await state.set_state(LotsFilter.lots)  # Установка состояния
    await state.set_data(default_values)  # Сброс данных к значениям по умолчанию
    UsersModel().add_user(message) # добавить пользователя в базу
    await message.answer(f'Hi!', reply_markup=start_keyboard())  # Отправка приветственного сообщения


# Обработчик кнопки "start"
@router.callback_query(F.data == "start")
async def escape(callback: types.CallbackQuery):
    await callback.message.edit_text(f'Hi!', reply_markup=start_keyboard())


# Обработчик кнопки "lots"
@router.callback_query(F.data == "lots")
async def lots(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(LotsFilter.lots)  # Установка состояния для лотов
    lots_data = await state.get_data()  # Получение данных состояния
    lots = Lot()  # Инициализация модели для работы с лотами
    lot = lots.get_data_from_storage(lots_data['region'], lots_data['category'])  # Получение данных лотов
    if lot:  # Если есть доступные лоты
        await state.update_data({'count': len(lot), 'lot_offset': 0, 'lots': lot})  # Обновление данных состояния
        text = get_text_data(lot[0])  # Формирование текста первого лота
        await callback.message.edit_text(text, reply_markup=lot_keyboard(0, len(lot)))  # Отображение лота
    else:
        await callback.message.edit_text('Нет данных по запросу.',
                                         reply_markup=start_keyboard())  # Сообщение об отсутствии данных


# Обработчик кнопки "filter" для выбора фильтров
@router.callback_query(F.data == 'filter')
async def filter(callback: types.CallbackQuery):
    await callback.message.edit_text('Выберите фильтр: ', reply_markup=filter_keyboard())  # Отображение меню фильтров


# Обработчик кнопки "region" для выбора региона
@router.callback_query(F.data == "region")
async def send_random_value(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(LotsFilter.region)  # Установка состояния выбора региона
    await state.update_data(offset=0)  # Сброс смещения к нулю
    await callback.message.edit_text(text="Введите регион",
                                     reply_markup=region_keyboard())  # Вывод клавиатуры для выбора региона


# Обработчик кнопки "category" для выбора категории
@router.callback_query(F.data == "category")
async def category(callback: types.CallbackQuery):
    await callback.message.edit_text(text="Выберите категорию:",
                                     reply_markup=category_keyboard())  # Отображение меню категорий


# Обработчик выбора конкретного региона из списка
@router.callback_query(F.data.split('?')[0] == 'region')
async def region(callback: types.CallbackQuery, state: FSMContext):
    code_region = callback.data.split('?')[1]  # Извлечение кода региона из данных колбека
    region = data.subRF[code_region]  # Получение данных о регионе из справочника
    await state.update_data(region=region['searchCode'])  # Сохранение кода региона в состоянии
    await callback.message.edit_text(f'Выбран регион: {region["name"]}',
                                     reply_markup=filter_keyboard())  # Подтверждение выбора региона


# Обработчик выбора конкретной категории из списка
@router.callback_query(F.data.split('?')[0] == "category")
async def flat(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(LotsFilter.category)  # Установка состояния выбора категории
    text = ''
    category = callback.data.split('?')[1]  # Извлечение кода категории из данных колбека
    # В зависимости от выбранной категории сохраняются данные и отображается соответствующее сообщение
    if category == 'flat':
        await state.update_data(category=9)  # Установка категории "Недвижимость"
        text = 'Недвижимость'
    elif category == 'auto':
        await state.update_data(category=100001)  # Установка категории "Автомобили"
        text = 'Автомобили'
    await callback.message.edit_text(f'Выбрана категория: {text}', reply_markup=filter_keyboard())


# Обработчик кнопки "следующий лот" в просмотре лотов
@router.callback_query(F.data == '>>_lot')
async def next_lot(callback: types.CallbackQuery, state: FSMContext):
    await navigate(callback, state, 'lot_offset', 1,
                   lot_keyboard)  # Переход к следующему лоту с использованием функции navigate


# Обработчик кнопки "предыдущий лот" в просмотре лотов
@router.callback_query(F.data == '<<_lot')
async def prev_lot(callback: types.CallbackQuery, state: FSMContext):
    await navigate(callback, state, 'lot_offset', -1,
                   lot_keyboard)  # Переход к предыдущему лоту с использованием функции navigate


# Обработчик кнопки "вперед" в просмотре регионов
@router.callback_query(F.data == ">>")
async def next_region(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(LotsFilter.region) # Установка состояния
    offset = await state.get_value('offset') + 1 # Смещение "страницы"
    await state.update_data(offset=offset) # Обновление параметра
    await callback.message.edit_text(text="Введите регион", # Переход к следующему списку
                                     reply_markup=region_keyboard(await state.get_value('offset')))

# Обработчик кнопки "назад" в просмотре регионов
@router.callback_query(F.data == "<<")
async def prev_region(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(LotsFilter.region) # Установка состояния
    offset = await state.get_value('offset') - 1 # Смещение "страницы"
    await state.update_data(offset=offset) # Обновление параметра
    await callback.message.edit_text(text="Введите регион", # Переход к предыдущему списку
                                     reply_markup=region_keyboard(await state.get_value('offset')))

# Обработчик кнопки "анализ" для анализа текущего лота
@router.callback_query(F.data == "analyze")
async def analyze(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(LotsFilter.region)  # Установка состояния выбора региона (возможно, для обновления)
    state_data = await state.get_data()  # Получение данных состояния
    offset = state_data['lot_offset']  # Текущее смещение лота
    lot = state_data['lots'][offset]  # Получение текущего лота
    text = get_text_data(state_data['lots'][offset]) + '\n'  # Формирование текста для лота

    # Анализ данных лота в зависимости от его категории
    if state_data['category'] == 9:  # Если категория - недвижимость
        lot_info = Lot().info_flat(lot['id'])[0]  # Получение информации о лоте
        data = get_data_cian(lot_info['flat_type'], lot['region'], lot_info['square'])  # Получение данных анализа
    elif state_data['category'] == 100001:  # Если категория - автомобили
        lot_info = Lot().info_auto(lot['id'])[0]  # Получение информации о лоте
        data = get_data_auto(lot['region'], lot_info['brand'], lot_info['model'],
                             lot_info['year'])  # Получение данных анализа

    # Добавление в избранное, если выполнены условия
    favorite = add_favorite(lot['price'], data[1], lot['id']) if len(data) == 3 else ""
    await callback.message.edit_text(text=text + favorite + '\n'.join(data), reply_markup=lot_keyboard(offset,
                                                                                                       state_data[
                                                                                                           'count']))  # Отображение данных анализа


# Обработчик кнопки "Избранное" для просмотра избранных лотов
@router.callback_query(F.data == "look_favorite")
async def look_favorite(callback: types.CallbackQuery, state: FSMContext):
    lots = Lot()  # Создание объекта модели для работы с лотами
    lot = lots.get_favorites()  # Получение списка избранных лотов
    await state.update_data({'count': len(lot), 'lot_offset': 0, 'lots': lot})  # Обновление данных состояния
    num = await state.get_value('lot_offset')  # Текущее смещение
    count = await state.get_value('count')  # Общее количество избранных
    if lot:  # Если есть избранные лоты
        text = get_text_data(lot[num])  # Формирование текста текущего лота
        await callback.message.edit_text(text, reply_markup=favorite_keyboard(num, count))  # Отображение лота
    else:
        await callback.message.edit_text('Нет данных по запросу.',
                                         reply_markup=nd_keyboard())  # Сообщение об отсутствии избранных


# Обработчики кнопок для навигации по избранным лотам
@router.callback_query(F.data == '>>_favorite')
async def next_favorite(callback: types.CallbackQuery, state: FSMContext):
    await navigate(callback, state, 'lot_offset', 1, favorite_keyboard)  # Переход к следующему избранному лоту


@router.callback_query(F.data == '<<_favorite')
async def prev_favorite(callback: types.CallbackQuery, state: FSMContext):
    await navigate(callback, state, 'lot_offset', -1, favorite_keyboard)  # Переход к предыдущему избранному лоту


# Обработчик кнопки "добавить в избранное" для текущего лота
@router.callback_query(F.data == 'favorite')
async def favorite(callback: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()  # Получение данных состояния
    lot = state_data['lots'][state_data['lot_offset']]  # Получение текущего лота
    # Добавление в избранное или сообщение о том, что уже добавлено
    if Lot().add_favorite(lot['id']):
        text = '\n\nДобавлено в избранное'
    else:
        text = '\n\nУже есть в избранном'
    text = get_text_data(lot) + text  # Формирование текста лота
    await callback.message.edit_text(text, reply_markup=lot_keyboard(state_data['lot_offset'],
                                                                     state_data['count']))  # Обновление текста


# Обработчик кнопки "удалить из избранного"
@router.callback_query(F.data == 'delete_favorite')
async def delete_favorite(callback: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()  # Получение данных состояния
    lots = Lot()  # Создание объекта модели
    lots.delete_favorites(state_data['lots'][state_data['lot_offset']]['id'])  # Удаление лота из избранного
    lot = lots.get_favorites()  # Обновление списка избранных
    await state.update_data({'count': len(lot), 'lot_offset': 0, 'lots': lot})  # Сброс состояния
    text = 'Удалено из избранного'  # Сообщение об удалении
    await callback.message.edit_text(text, reply_markup=create_keyboard([], prev='look_favorite'))  # Отображение сообщения


@router.callback_query(F.data == 'refresh_lots')
async def refresh(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(LotsFilter.lots)  # Установка состояния для лотов
    lots_data = await state.get_data()  # Получение данных состояния
    lots = Lot()  # Инициализация модели для работы с лотами
    pages = get_pages(lots_data['region'], lots_data['category'])
    for i in range(pages):
        await callback.message.edit_text(f'Обработка {i}/{pages}')
        if lots.add_lots(lots_data['region'], lots_data['category'], i).get('exit', False):
            break

    await callback.message.edit_text('Лоты обновлены!',
                                         reply_markup=start_keyboard())  # Сообщение об отсутствии данных