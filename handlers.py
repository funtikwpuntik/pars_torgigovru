from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

import data
from model import Lot, get_text_data, UsersModel
from scrap_auto import get_data_auto
from scrap_cian import get_data_cian


class LotsFilter(StatesGroup):
    region = State()
    category = State()
    lots = State()


default_values = {
    'region': 77,
    'category': 9,
    'offset': 0,
    'lot_offset': 0,
    'count': 0,
    'lots': [],
}
router = Router()

def add_favorite(lot_price, price, lot_id):
    if float(lot_price) * 1.35744 <= float(price):
        Lot().add_favorite(lot_id)
        return '\nДобавлено в избранное\n'
    return ''

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
    return create_keyboard([("Автомобили", "auto"), ("Недвижимость", "flat")], 2)


def region_keyboard(page: int):
    offset = page * 20
    regions = list(data.subRF.items())[offset:offset + 20]
    buttons = [(value, f"region?{key}") for key, value in regions]

    if offset > 0:
        buttons.append(("<<", "<<"))
    if offset + 20 < len(data.subRF):
        buttons.append((">>", ">>"))

    return create_keyboard(buttons, row_width=2)


def lot_keyboard(offset, count):
    buttons = [('Анализ', 'analyze'), ('Добавить в избранное', 'favorite'), ('Избранное', 'look_favorite')]
    if offset > 0:
        buttons.append(("<<", "<<_lot"))
    if offset < count - 1:
        buttons.append((">>", ">>_lot"))
    return create_keyboard(buttons, 3)

def favorite_keyboard(offset, count):
    buttons = [('Удалить из избранного', 'delete_favorite')]
    if offset > 0:
        buttons.append(("<<", "<<_favorite"))
    if offset < count - 1:
        buttons.append((">>", ">>_favorite"))
    return create_keyboard(buttons, 2)

def nd_keyboard():
    buttons = [('Лоты', 'lots')]
    return create_keyboard(buttons)

def start_keyboard():
    buttons = [('Лоты', 'lots'), ('Избранное', 'look_favorite')]
    return create_keyboard(buttons, 2)


@router.message(Command("start"))
async def start(message: Message, state: FSMContext):
    await state.set_state(LotsFilter.lots)
    await state.set_data(default_values)
    await message.answer(f'Hi!', reply_markup=start_keyboard())
    print(UsersModel().add_user(message))


@router.callback_query(F.data == "lots")
async def lots(message: Message, state: FSMContext):
    await state.set_state(LotsFilter.lots)
    lots_data = await state.get_data()
    lots = Lot()
    lots.add_lots(lots_data['region'], lots_data['category'])
    lot = lots.get_data_from_storage(lots_data['region'], lots_data['category'])
    if lot:
        await state.update_data({'count': len(lot), 'lot_offset': 0, 'lots': lot})
        num = await state.get_value('lot_offset')
        count = await state.get_value('count')
        text = get_text_data(lot[num])
        await message.answer(text, reply_markup=lot_keyboard(num, count))
    else:
        await message.answer('Нет данных по запросу.')


@router.message(Command('filter'))
async def filter(message: Message):
    await message.answer('Выберите фильтр: ', reply_markup=filter_keyboard())


@router.callback_query(F.data == "region")
async def send_random_value(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(LotsFilter.region)

    await callback.message.edit_text(text="Введите регион",
                                     reply_markup=region_keyboard(await state.get_value('offset')))


@router.callback_query(F.data == "category")
async def category(callback: types.CallbackQuery):
    await callback.message.edit_text(text="Выберите категорию:", reply_markup=category_keyboard())


@router.message(LotsFilter.region)
async def region(message: Message, state: FSMContext):
    await state.update_data(region=message.text)
    await message.answer(f'Выбран регион: {message.text}')


@router.callback_query(F.data == "flat")
async def flat(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(LotsFilter.category)
    await state.update_data(category=9)
    await callback.message.edit_text(f'Выбрана категория: Недвижимость')


@router.callback_query(F.data == "auto")
async def auto(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(LotsFilter.category)
    await state.update_data(category=100001)
    await callback.message.edit_text(f'Выбрана категория: Автомобили')


@router.callback_query(F.data == '>>_lot')
async def next_lot(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(LotsFilter.lots)
    lots_data = await state.get_data()
    offset = lots_data['lot_offset'] + 1
    await state.update_data(lot_offset=offset)
    lot = lots_data['lots'][offset]
    text = get_text_data(lot)
    await callback.message.edit_text(text, reply_markup=lot_keyboard(offset, lots_data['count']))


@router.callback_query(F.data == '<<_lot')
async def prev_lot(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(LotsFilter.lots)
    lots_data = await state.get_data()
    offset = lots_data['lot_offset'] - 1
    await state.update_data(lot_offset=offset)
    lot = lots_data['lots'][offset]
    text = get_text_data(lot)
    await callback.message.edit_text(text, reply_markup=lot_keyboard(offset, lots_data['count']))


@router.callback_query(F.data == ">>")
async def next_region(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(LotsFilter.region)
    offset = await state.get_value('offset') + 1
    await state.update_data(offset=offset)
    await callback.message.edit_text(text="Введите регион",
                                     reply_markup=region_keyboard(await state.get_value('offset')))


@router.callback_query(F.data == "<<")
async def prev_region(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(LotsFilter.region)
    offset = await state.get_value('offset') - 1
    await state.update_data(offset=offset)
    await callback.message.edit_text(text="Введите регион",
                                     reply_markup=region_keyboard(await state.get_value('offset')))


@router.callback_query(F.data == "analyze")
async def analyze(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(LotsFilter.region)

    state_data = await state.get_data()
    offset = state_data['lot_offset']
    lot = state_data['lots'][offset]

    text = get_text_data(state_data['lots'][offset])+'\n'
    if state_data['category'] == 9:
        lot_info = Lot().info_flat(lot['id'])[0]
        data = get_data_cian(lot_info['flat_type'], lot['region'], lot_info['square'])

    elif state_data['category'] == 100001:
        lot_info = Lot().info_auto(lot['id'])[0]
        data = get_data_auto(lot['region'], lot_info['brand'], lot_info['model'], lot_info['year'])

    favorite = add_favorite(lot['price'], data[1], lot['id']) if len(data) == 3 else ""
    await callback.message.edit_text(text=text + favorite +'\n'.join(data),
                                     reply_markup=lot_keyboard(offset, state_data['count']))



@router.callback_query(F.data.startswith("region?"))
async def select_region(callback: types.CallbackQuery, state: FSMContext):
    region_id = int(callback.data.split("?")[1])
    await state.update_data(region=region_id)
    await callback.message.edit_text(f"Выбран регион: {region_id}")


@router.callback_query(F.data == "look_favorite")
async def look_favorite(callback: types.CallbackQuery, state: FSMContext):
    lots = Lot()
    lot = lots.get_favorites()
    await state.update_data({'count': len(lot), 'lot_offset': 0, 'lots': lot})
    num = await state.get_value('lot_offset')
    count = await state.get_value('count')
    if lot:
        text = get_text_data(lot[num])
        await callback.message.edit_text(text, reply_markup=favorite_keyboard(num, count))
    else:
        await callback.message.edit_text('Нет данных по запросу.', reply_markup=nd_keyboard())



@router.callback_query(F.data == '>>_favorite')
async def next_favorite(callback: types.CallbackQuery, state: FSMContext):
    lots_data = await state.get_data()
    offset = lots_data['lot_offset'] + 1
    await state.update_data(lot_offset=offset)
    lot = lots_data['lots'][offset]
    text = get_text_data(lot)
    await callback.message.edit_text(text, reply_markup=favorite_keyboard(offset, lots_data['count']))


@router.callback_query(F.data == '<<_favorite')
async def prev_favorite(callback: types.CallbackQuery, state: FSMContext):
    lots_data = await state.get_data()
    offset = lots_data['lot_offset'] - 1
    await state.update_data(lot_offset=offset)
    lot = lots_data['lots'][offset]
    text = get_text_data(lot)
    await callback.message.edit_text(text, reply_markup=favorite_keyboard(offset, lots_data['count']))

@router.callback_query(F.data == 'favorite')
async def favorite(callback: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    lot = state_data['lots'][state_data['lot_offset']]
    if Lot().add_favorite(lot['id']):
        text = '\n\nДобавлено в избранное'
    else:
        text = '\n\nУже есть в избранном'
    text = get_text_data(lot) + text
    await callback.message.edit_text(text, reply_markup=lot_keyboard(state_data['lot_offset'], state_data['count']))


@router.callback_query(F.data == 'delete_favorite')
async def delete_favorite(callback: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    lots = Lot()
    lots.delete_favorites(state_data['lots'][state_data['lot_offset']]['id'])
    lot = lots.get_favorites()
    await state.update_data({'count': len(lot), 'lot_offset': 0, 'lots': lot})
    text = 'Удалено из избранного'
    await callback.message.edit_text(text, reply_markup=favorite_keyboard(state_data['lot_offset'], state_data['count']))