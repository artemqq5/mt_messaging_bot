from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove, Message

from data.other.constants import VIEW_ALL_GROUP
from data.repositories.AdminRepository import AdminRepository
from data.repositories.ChatRepository import ChatRepository
from domain.filters.IsAdmin import IsAdminFilter
from domain.middlewares.IsPrivateChatAdmin import IsPrivateChatAdmin
from presentation.keyboard.admin_ import kb_main
from states.ShowGroup import ShowGroupState

router = Router()


# @router.message(F.text == VIEW_ALL_GROUP)
# async def choice_type_groups(message: Message, state: FSMContext):
#     await state.set_state(ShowGroupState.TypeGroup)
#     await message.answer("Оберіть тип групи", reply_markup=kb_type_group.as_markup())
#
#
# @router.message()
# async def show_unspecified_group(message: Message, state: FSMContext):
#     group = ChatRepository().all_chats()
#     await message.answer("Групи", reply_markup=kb_groups(group).as_markup())
