from aiogram import Router, F, Bot
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from data.other.accesses import access_admin_to_chat, TypeOfAdmins, TypeOfChats
from data.other.constants import VIEW_ALL_GROUP, UNSPECIFIED_GROUPS
from data.repositories.AdminRepository import AdminRepository
from data.repositories.ChatRepository import ChatRepository
from domain.filters.IsMainAdmin import IsMainAdminFilter
from presentation.keyboard.admin_ import kb_type_group, kb_groups, GroupCallback, kb_main, generate_pagination_groups, \
    GroupPageCallback
from states.ShowGroup import ShowGroupState

router = Router()


@router.message(F.text == VIEW_ALL_GROUP)
async def choice_type_groups(message: Message, state: FSMContext):
    admin = AdminRepository().is_admin(message.chat.id)
    await state.set_state(ShowGroupState.TypeGroup)
    await message.answer("Оберіть тип групи", reply_markup=kb_type_group(admin).as_markup())


@router.message(ShowGroupState.TypeGroup, IsMainAdminFilter(), F.text == UNSPECIFIED_GROUPS)
async def show_specific_groups(message: Message, state: FSMContext):
    chats = ChatRepository().unspecified_chats()
    await state.update_data(chats=chats)

    await message.answer(
        f"Групи за типом <b>{message.text}</b>:",
        reply_markup=generate_pagination_groups(current_page=1, groups=chats).as_markup()
    )


@router.message(ShowGroupState.TypeGroup)
async def show_groups(message: Message, state: FSMContext):
    admin = AdminRepository().is_admin(message.chat.id)
    if message.text not in access_admin_to_chat[admin['role']]:
        return
    if message.text == TypeOfChats.ALL.value:
        chats = ChatRepository().all_chats()
    else:
        chats = ChatRepository().chat_by_type(message.text)

    await state.update_data(chats=chats)

    await message.answer(
        f"Групи за типом <b>{message.text}</b>:",
        reply_markup=generate_pagination_groups(current_page=1, groups=chats).as_markup()
    )


@router.callback_query(GroupPageCallback.filter())
async def page_group_listener(callback: CallbackQuery, state: FSMContext):
    page = int(callback.data.split(":")[1])
    data = await state.get_data()
    await callback.message.edit_reply_markup(
        reply_markup=generate_pagination_groups(current_page=page, groups=data['chats']).as_markup()
    )


@router.callback_query(GroupCallback.filter())
async def about_group(callback: CallbackQuery, bot: Bot):
    id_ = callback.data.split(":")[1]
    group = ChatRepository().get_chat(id_)

    categories = [str(f"{i}\n").replace("_", " ") for i in group if str(group[i]) == '1']

    if len(categories) > 0:
        categories = ''.join(categories)
    else:
        categories = "Невизначена група\n"

    info = f"*{group['title']}* (`{group['group_id']}`):\n\n"
    info += f"*Категорії групи:*\n{categories}\n"
    info += f"*Запрошувальне посилання:* {group['link']}\n"
    info += f"Група додана: {group['time']}"

    admin = AdminRepository().is_admin(callback.from_user.id)
    await callback.message.answer(info, reply_markup=kb_type_group(admin).as_markup(), parse_mode=ParseMode.MARKDOWN)
