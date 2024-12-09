from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from model import Lot, get_text_data, UsersModel
from utils.keyboards import *
from utils.scrap_auto import get_data_auto
from utils.scrap_cian import get_data_cian


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






async def navigate(callback: types.CallbackQuery, state: FSMContext, key: str, direction: int, keyboard_fn):
    state_data = await state.get_data()
    offset = state_data[key] + direction
    await state.update_data({key: offset})
    lot = state_data['lots'][offset]
    text = get_text_data(lot)
    await callback.message.edit_text(text, reply_markup=keyboard_fn(offset, state_data['count']))


async def update_state_and_data(state: FSMContext, new_state: State, data: dict):
    await state.set_state(new_state)
    await state.update_data(data)

@router.message(Command("start"))
async def start(message: Message, state: FSMContext):
    await state.set_state(LotsFilter.lots)
    await state.set_data(default_values)
    await message.answer(f'Hi!', reply_markup=start_keyboard())
    print(UsersModel().add_user(message))


@router.callback_query(F.data == "lots")
async def lots(callback: types.CallbackQuery, state: FSMContext):
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
        await callback.message.edit_text(text, reply_markup=lot_keyboard(num, count))
    else:
        await callback.message.edit_text('Нет данных по запросу.', reply_markup=start_keyboard())


@router.callback_query(F.data == 'filter')
async def filter(callback: types.CallbackQuery):
    await callback.message.edit_text('Выберите фильтр: ', reply_markup=filter_keyboard())


@router.callback_query(F.data == "region")
async def send_random_value(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(LotsFilter.region)
    await state.update_data(offset=0)
    await callback.message.edit_text(text="Введите регион",
                                     reply_markup=region_keyboard())


@router.callback_query(F.data == "category")
async def category(callback: types.CallbackQuery):
    await callback.message.edit_text(text="Выберите категорию:", reply_markup=category_keyboard())


@router.callback_query(F.data.split('?')[0] == 'region')
async def region(callback: types.CallbackQuery, state: FSMContext):
    code_region = callback.data.split('?')[1]
    region = data.subRF[code_region]
    await state.update_data(region=region['searchCode'])
    await callback.message.edit_text(f'Выбран регион: {region["name"]}', reply_markup=start_keyboard())


@router.callback_query(F.data.split('?')[0] == "category")
async def flat(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(LotsFilter.category)
    text = ''
    category = callback.data.split('?')[1]
    if category == 'flat':
        await state.update_data(category=9)
        text = 'Недвижимость'
    elif category == 'auto':
        await state.update_data(category=100001)
        text = 'Автомобили'
    await callback.message.edit_text(f'Выбрана категория: {text}', reply_markup=start_keyboard())

@router.callback_query(F.data == '>>_lot')
async def next_lot(callback: types.CallbackQuery, state: FSMContext):
    await navigate(callback, state, 'lot_offset', 1, lot_keyboard)


@router.callback_query(F.data == '<<_lot')
async def prev_lot(callback: types.CallbackQuery, state: FSMContext):
    await navigate(callback, state, 'lot_offset', -1, lot_keyboard)


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
    await navigate(callback, state, 'lot_offset', 1, favorite_keyboard)


@router.callback_query(F.data == '<<_favorite')
async def prev_favorite(callback: types.CallbackQuery, state: FSMContext):
    await navigate(callback, state, 'lot_offset', -1, favorite_keyboard)

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
    await callback.message.edit_text(text, reply_markup=nd_keyboard())