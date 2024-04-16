from aiogram import Router, types, F, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from data.other.constants import CANCEL, CANCEL_SUCCESS, BUG_REPORT
from domain.filters.IsGroup import IsGropFilter
from domain.filters.IsMainAdmin import IsMainAdminFilter
from domain.middlewares.IsPrivateChatAdmin import IsPrivateChatAdmin
from domain.routers.admin.chat.menu import show_, message_, statistic_
from domain.tools.BotCheckChat import check_bot_membership
from presentation.keyboard.admin_ import kb_main

router = Router()
router.include_routers(
    show_.router,
    message_.router,
    statistic_.router
)

router.message.middleware(IsPrivateChatAdmin())
router.callback_query.middleware(IsPrivateChatAdmin())


@router.message(Command('start'), IsGropFilter(False))
async def start(message: types.Message, state: FSMContext):
    await state.clear()

    await message.answer("<b>Привіт, це бот для розсилки сповіщень</b>\n\n"
                         "Щоб додати групу до розсилки: \n"
                         "1) Додай туди бота і назнач його адміном\n"
                         "2) Напиши команду <code>/start</code> в групі\n"
                         "3) Задай статус для групи <code>/agency_fb 1</code> це задасть тип Агнества Фейсбук.\n"
                         "Щоб прибрати статус <code>/agency_fb</code>",
                         reply_markup=kb_main.as_markup())


@router.message(F.text == CANCEL)
async def cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(CANCEL_SUCCESS, reply_markup=kb_main.as_markup())
