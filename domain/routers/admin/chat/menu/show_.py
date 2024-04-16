from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from data.other.accesses import access_admin_to_chat, TypeOfAdmins
from data.other.constants import VIEW_ALL_GROUP, UNSPECIFIED_GROUPS, ALL_GROUPS
from data.repositories.AdminRepository import AdminRepository
from data.repositories.ChatRepository import ChatRepository
from domain.filters.IsMainAdmin import IsMainAdminFilter
from presentation.keyboard.admin_ import kb_type_group, kb_groups, GroupCalback, kb_main
from states.ShowGroup import ShowGroupState

router = Router()


@router.message(F.text == VIEW_ALL_GROUP)
async def choice_type_groups(message: Message, state: FSMContext):
    admin = AdminRepository().is_admin(message.chat.id)
    await state.set_state(ShowGroupState.TypeGroup)
    await message.answer("Оберіть тип групи", reply_markup=kb_type_group(admin).as_markup())


@router.message(ShowGroupState.TypeGroup, IsMainAdminFilter(), F.text.in_((UNSPECIFIED_GROUPS, ALL_GROUPS)))
async def show_specific_groups(message: Message, state: FSMContext):
    if message.text == UNSPECIFIED_GROUPS:
        chats = ChatRepository().unspecified_chats()
    else:
        chats = ChatRepository().all_chats()

    await message.answer(f"Групи за типом <b>{message.text}</b>:", reply_markup=kb_groups(chats).as_markup())


@router.message(ShowGroupState.TypeGroup)
async def show_groups(message: Message, state: FSMContext):
    admin = AdminRepository().is_admin(message.chat.id)
    if message.text not in access_admin_to_chat[admin['role']]:
        return

    chats = ChatRepository().chat_by_type(message.text)
    await message.answer(f"Групи за типом <b>{message.text}</b>:", reply_markup=kb_groups(chats).as_markup())


@router.callback_query(GroupCalback.filter())
async def about_group(callback: CallbackQuery, bot: Bot):
    id_ = callback.data.split(":")[1]
    group = ChatRepository().get_chat(id_)

    categoties = [str(f"{i}\n").replace("_", " ") for i in group if str(group[i]) == '1']

    if len(categoties) > 0:
        categoties = ''.join(categoties)
    else:
        categoties = "Невизначена група\n"

    info = f"{group['title']} (<code>{group['group_id']}</code>):\n\n"
    info += f"<b>Категорії групи:</b> \n{categoties}\n"
    info += f"<b>Запрошувальне посилання:</b> {group['link']}\n"
    info += f"Група додана: {group['time']}"

    admin = AdminRepository().is_admin(callback.from_user.id)
    await callback.message.answer(info, reply_markup=kb_type_group(admin).as_markup())
