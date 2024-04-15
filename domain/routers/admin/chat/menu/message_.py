from aiogram import Router, F, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from data.other.constants import MESSAGING_GROP, SKIP, SEND
from data.repositories.AdminRepository import AdminRepository
from domain.filters.IsAdmin import IsAdminFilter
from domain.middlewares.IsPrivateChatAdmin import IsPrivateChatAdmin
from notify.message_spam import spam_all_groups
from presentation.keyboard.admin_ import kb_main, kb_cancel, kb_skip, kb_send, kb_access_category
from states.SendMessage import SendMessageState

router = Router()


@router.message(F.text == MESSAGING_GROP)
async def start_create_message(message: types.Message, state: FSMContext):
    admin = AdminRepository().is_admin(message.chat.id)
    await state.set_state(SendMessageState.category)
    await message.answer('Оберіть категорію групи з наявних вашому доступу: ',
                         reply_markup=kb_access_category(admin).as_markup())


@router.message(SendMessageState.category)
async def set_category(message: types.Message, state: FSMContext):
    await state.update_data(category=message.text)
    await state.set_state(SendMessageState.message)
    await message.answer('Введіть свій текст для розсилки: ', reply_markup=kb_cancel.as_markup())


@router.message(SendMessageState.message)
async def set_message(message: types.Message, state: FSMContext):
    await state.update_data(message=message.html_text)
    await state.set_state(SendMessageState.photo)
    await message.answer(
        "Відправте фото, відео або гіфку (формат з стисненням, а не файл)", reply_markup=kb_skip.as_markup()
    )


@router.message(SendMessageState.photo, (F.photo | F.animation | F.video | (F.text & F.text == SKIP)))
async def set_photo(message: types.Message, state: FSMContext):
    await state.set_state(SendMessageState.preview)

    if message.content_type == 'photo':
        await state.update_data(photo=message.photo[-1].file_id)
        data = await state.get_data()
        await message.answer_photo(data['photo'], caption=data['message'], reply_markup=kb_send.as_markup())

    elif message.content_type == 'animation':
        await state.update_data(animation=message.document.file_id)
        data = await state.get_data()
        await message.answer_animation(data['animation'], caption=data['message'], reply_markup=kb_send.as_markup())

    elif message.content_type == 'video':
        await state.update_data(video=message.video.file_id)
        data = await state.get_data()
        await message.answer_video(data['video'], caption=data['message'], reply_markup=kb_send.as_markup())
    else:
        data = await state.get_data()
        await message.answer(data['message'], reply_markup=kb_send.as_markup())


@router.message(SendMessageState.preview, F.text == SEND)
async def message_preview(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    await spam_all_groups(data, message, data.get('category', None))
