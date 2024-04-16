from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder

from data.other.constants import MESSAGING_GROP, SKIP, SEND, YES
from data.repositories.AdminRepository import AdminRepository
from domain.tools.MessageSpamTool import spam_all_groups
from presentation.keyboard.admin_ import kb_cancel, kb_skip, kb_send, kb_quetion, kb_messaging_category
from states.SendMessage import SendMessageState

router = Router()


@router.message(F.text == MESSAGING_GROP)
async def start_create_message(message: types.Message, state: FSMContext):
    admin = AdminRepository().is_admin(message.chat.id)
    await state.set_state(SendMessageState.category)
    await message.answer('Оберіть категорію групи з наявних вашому доступу: ',
                         reply_markup=kb_messaging_category(admin).as_markup())


@router.message(SendMessageState.category)
async def set_category(message: types.Message, state: FSMContext):
    await state.update_data(category=message.text)
    await state.set_state(SendMessageState.message)
    await message.answer('Введіть свій текст для розсилки: ', reply_markup=kb_cancel.as_markup())


@router.message(SendMessageState.message)
async def set_message(message: types.Message, state: FSMContext):
    await state.update_data(message=message.html_text)
    await state.set_state(SendMessageState.button)
    await message.answer("Бажаєте додати кнопку?", reply_markup=kb_quetion.as_markup())


@router.message(SendMessageState.button, F.text.in_((SKIP, YES)))
async def set_button(message: types.Message, state: FSMContext):
    if message.text == SKIP:
        await state.set_state(SendMessageState.photo)
        await message.answer("Відправте фото, відео або гіфку (формат з стисненням, а не файл)",
                             reply_markup=kb_skip.as_markup())
        return

    await state.set_state(SendMessageState.buttonText)
    await message.answer(
        "Вигадайте текст для кнопки(50 символів) або залиште дефолтний", reply_markup=kb_skip.as_markup()
    )


@router.message(SendMessageState.buttonText)
async def set_button_text(message: types.Message, state: FSMContext):
    if len(message.text) > 50:
        await message.answer("До 50 символів!", reply_markup=kb_skip.as_markup())
        return

    if message.text == SKIP:
        await state.update_data(btn_text="Перейти")
    else:
        await state.update_data(btn_text=message.text)

    await state.set_state(SendMessageState.buttonUrl)
    await message.answer("Відправте url куди перенправити", reply_markup=kb_cancel.as_markup())


@router.message(SendMessageState.buttonUrl)
async def set_button_url(message: types.Message, state: FSMContext):
    await state.update_data(btn_url=message.text)
    await state.set_state(SendMessageState.photo)
    await message.answer("Відправте фото, відео або гіфку (формат з стисненням, а не файл)",
                         reply_markup=kb_skip.as_markup())


@router.message(SendMessageState.photo, (F.photo | F.animation | F.video | (F.text & F.text == SKIP)))
async def set_photo(message: types.Message, state: FSMContext):
    await state.set_state(SendMessageState.preview)
    data = await state.get_data()
    if data.get('btn_text', None):
        kb = InlineKeyboardBuilder(
            markup=[[InlineKeyboardButton(text=data['btn_text'], url=data['btn_url'])]]).as_markup()
    else:
        kb = ReplyKeyboardRemove()

    if message.content_type == 'photo':
        await state.update_data(photo=message.photo[-1].file_id)
        data = await state.get_data()
        await message.answer_photo(data['photo'], caption=data['message'], reply_markup=kb)

    elif message.content_type == 'animation':
        await state.update_data(animation=message.document.file_id)
        data = await state.get_data()
        await message.answer_animation(data['animation'], caption=data['message'], reply_markup=kb)

    elif message.content_type == 'video':
        await state.update_data(video=message.video.file_id)
        data = await state.get_data()
        await message.answer_video(data['video'], caption=data['message'], reply_markup=kb)

    else:
        data = await state.get_data()
        await message.answer(data['message'], reply_markup=kb)

    await message.answer("Все окей?", reply_markup=kb_send.as_markup())


@router.message(SendMessageState.preview, F.text == SEND)
async def message_preview(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    await spam_all_groups(data, message, data.get('category', None))
