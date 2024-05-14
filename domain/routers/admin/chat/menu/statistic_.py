from aiogram import Router, F, Bot, types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from data.other.accesses import access_admin_to_chat, TypeOfAdmins
from data.other.constants import VIEW_ALL_GROUP, UNSPECIFIED_GROUPS, STATISTIC, BUG_REPORT
from data.repositories.AdminRepository import AdminRepository
from data.repositories.ChatRepository import ChatRepository
from data.repositories.UserRepository import UserRepository
from domain.filters.IsMainAdmin import IsMainAdminFilter
from domain.tools.BotCheckChat import check_bot_membership
from presentation.keyboard.admin_ import kb_type_group, kb_groups, GroupCallback, kb_main
from states.ShowGroup import ShowGroupState

router = Router()


@router.message(F.text == STATISTIC, IsMainAdminFilter())
async def statistic_info(message: Message, state: FSMContext):
    chats = ChatRepository().all_chats()
    users = UserRepository().get_users()

    info = "<b>Статистика по боту</b>\n\n"
    info += f"Всього груп додано до бота: {len(chats)}\n"
    info += f"Всього юзерів перехвачено і записано в базу: {len(users)}"

    await message.answer(info)


@router.message(F.text == STATISTIC)
async def statistic_info(message: Message, state: FSMContext):
    await message.answer("Немає доступу")


@router.message(F.text == BUG_REPORT, IsMainAdminFilter())
async def bug_report(message: types.Message, bot: Bot):
    await check_bot_membership(bot, message.from_user.id)


@router.message(F.text == BUG_REPORT)
async def bug_report(message: types.Message, bot: Bot):
    await message.answer("Немає доступу")
