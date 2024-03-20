from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, ParseMode

from notify.message_spam import spam_all_groups
from notify.send_back_check import send_back_check
from repository.user_rep import UserRep
from role.accesses import access_admin_to_chat
from states.state_message import StateMessage


def register_message_send_handler(dispatcher):
    dispatcher.register_message_handler(set_category, state=StateMessage.category)
    dispatcher.register_message_handler(set_message, state=StateMessage.message)
    dispatcher.register_message_handler(set_photo, state=StateMessage.photo, content_types=['photo', 'animation', 'video', 'text'])
    dispatcher.register_message_handler(send_message, state=StateMessage.check)


async def set_category(message: types.Message, state: FSMContext):
    admin = UserRep()._is_admin(message.chat.id)
    if admin is not None and message.text in access_admin_to_chat[admin['role']]:
        await state.update_data(category=message.text)
        await StateMessage().message.set()
        await message.answer(
            'Введіть свій текст для розсилки: ',
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        await state.reset_state()
        await message.answer("Відмовлено в доступі", reply_markup=ReplyKeyboardRemove())


async def set_message(message: types.Message, state: FSMContext):
    await state.update_data(message=message.html_text)
    await StateMessage.photo.set()
    await message.answer(
        "Відправте фото, відео фбо гіфку (формат з стисненням, а не файл), якщо потрібно",
        reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton("Пропустити")]], resize_keyboard=True)
    )


async def set_photo(message: types.Message, state: FSMContext):
    if message.content_type == 'text' and message.text == "Пропустити":
        await StateMessage.check.set()
        data = await state.get_data()

        await send_back_check(message, data)

    elif message.content_type == 'photo':
        await StateMessage.check.set()
        await state.update_data(type_sub_data='photo')
        await state.update_data(photo=message.photo[-1].file_id)
        data = await state.get_data()

        await send_back_check(message, data)

    elif message.content_type == 'animation':
        await StateMessage.check.set()
        await state.update_data(type_sub_data='gif')
        await state.update_data(gif=message.document.file_id)
        data = await state.get_data()

        await send_back_check(message, data)

    elif message.content_type == 'video':
        await StateMessage.check.set()
        await state.update_data(type_sub_data='video')
        await state.update_data(video=message.video.file_id)
        data = await state.get_data()

        await send_back_check(message, data)
    else:
        await message.answer("Некоректний ввід")


async def send_message(message: types.Message, state: FSMContext):
    if message.text == "Відправити":
        data = await state.get_data()
        await state.finish()
        await spam_all_groups(data, message, data.get('category', None))
    else:
        await message.answer("Некоректний ввід")
