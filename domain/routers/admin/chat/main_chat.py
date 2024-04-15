from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from data.other.constants import CANCEL, CANCEL_SUCCESS
from domain.filters.IsAdmin import IsAdminFilter
from domain.middlewares.IsPrivateChatAdmin import IsPrivateChatAdmin
from domain.routers.admin.chat.menu import show_, message_
from presentation.keyboard.admin_ import kb_main

router = Router()
router.include_routers(
    show_.router,
    message_.router
)

router.message.middleware(IsPrivateChatAdmin())
router.callback_query.middleware(IsPrivateChatAdmin())


@router.message(Command('start'), IsAdminFilter())
async def start(message: types.Message, state: FSMContext):
    await state.clear()

    await message.answer("<b>Привіт, це бот для розсилки сповіщень</b>\n\n"
                         "Щоб додати групу до розсилки: \n"
                         "1) Додай туди бота і назнач його адміном\n"
                         "2) Перейди в пункт \"переглянути групи\" і задай тип чату який тобі потрібен, можеш навіть декілька",
                         reply_markup=kb_main.as_markup())


@router.message(F.text == CANCEL)
async def cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(CANCEL_SUCCESS, reply_markup=kb_main.as_markup())
