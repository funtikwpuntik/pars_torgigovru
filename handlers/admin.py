from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from filters.filter import ChatFilter
from storage import UsersStorage
from utils.keyboards import admin_keyboard

router = Router()
router.message.filter(ChatFilter([297871511]))


# Обработчик команды
@router.message(Command('admin'))
async def admin(message: Message):
    users = UsersStorage().get_users()
    await message.answer('Какого пользователя необходимо удалить?', reply_markup=admin_keyboard(users))


# Обработчик удаления пользователя
@router.callback_query(F.data.split('?')[0] == 'delete')
async def delete(callback: CallbackQuery):
    us = UsersStorage()
    us.delete_user(int(callback.data.split('?')[1]))
    users = us.get_users()
    await callback.message.edit_text('Пользователь удален.\nУдалить кого-нибудь еще?',
                                     reply_markup=admin_keyboard(users))
