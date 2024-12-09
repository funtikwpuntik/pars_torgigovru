from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from storage import UsersStorage
from filter import ChatFilter
router = Router()
router.message.filter(ChatFilter([297871511]))

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

def admin_keyboard(users):
    buttons = [
        (f"{user['name']}\t{user['username']}", f"delete?{user['id']}") for user in users
    ]
    return create_keyboard(buttons)
@router.message(Command('admin'))
async def admin(message: Message):
    users = UsersStorage().get_users()
    await message.answer('Какого пользователя необходимо удалить?', reply_markup=admin_keyboard(users))



@router.callback_query(F.data.split('?')[0] == 'delete')
async def delete(callback: CallbackQuery):
    us = UsersStorage()
    us.delete_user(int(callback.data.split('?')[1]))
    users = us.get_users()
    await callback.message.edit_text('Пользователь удален.\nУдалить кого-нибудь еще?', reply_markup=admin_keyboard(users))

