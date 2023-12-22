from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor

from cfg import BOT_TOKEN_ID
from database import MyDataBase
from notify.message_spam import spam_all_groups
from states.state_message import StateMessage

storage = MemoryStorage()
bot = Bot(token=BOT_TOKEN_ID, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=['start'])
async def welcome(message: types.Message, state='*'):
    # cancel state if not None
    current_state = await state.get_state()
    if current_state is not None:
        await state.reset_state()
        await message.answer("Операцію було скасовано")
    else:
        print(message.chat.type)
        if message.chat.type in [types.ChatType.GROUP, types.ChatType.SUPER_GROUP]:
            if MyDataBase().is_admin(message['from']['id']) is not None:
                result = MyDataBase().add_chat(message.chat.id, message.chat.title)
                if result is not None:
                    await message.answer("Група щойно була додана")
                else:
                    await message.answer("Група була додана ще до цього")
            else:
                await message.answer("Відмовлено в доступі")
        elif message.chat.type in [types.ChatType.PRIVATE, ]:
            if MyDataBase().is_admin(message['from']['id']) is not None:
                await message.answer("<b>Привіт, це бот для розсилки сповіщень</b>\n\n"
                                     "Щоб додати групу в розсилку, додайте до неї цього бота як адміна та введіть команду /start\n\n"
                                     "Щоб відправити повідомлення всім групам, введіть команду /message")
            else:
                await message.answer("Зареєструйся спочатку")


@dp.message_handler(commands=['message'])
async def send_messeging_to_all(message: types.Message):
    if message.chat.type in [types.ChatType.PRIVATE, ]:
        if MyDataBase().is_admin(message.chat.id) is not None:
            await StateMessage().message.set()
            await message.answer("Введіть свій текст для розсилки: ")
        else:
            await message.answer("Відмовлено в доступі")


@dp.message_handler(state=StateMessage.message)
async def set_message(message: types.Message, state: FSMContext):
    await state.update_data(message=message.text)
    await StateMessage.photo.set()
    await message.answer(
        "Відправте фото (саме формат фото, а не файл), якщо потрібно",
        reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton("Пропустити")]], resize_keyboard=True)
    )


@dp.message_handler(content_types=['photo', 'text'], state=StateMessage.photo)
async def set_message(message: types.Message, state: FSMContext):
    if message.text == "Пропустити":
        await StateMessage.check.set()
        data = await state.get_data()
        await message.answer(
            data['message'],
            reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton("Відправити")]], resize_keyboard=True)
        )
    elif message.photo.__len__() > 0:
        await StateMessage.check.set()
        await state.update_data(photo=message.photo[-1].file_id)
        data = await state.get_data()
        await message.answer_photo(
            data['photo'],
            caption=data['message'],
            reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton("Відправити")]], resize_keyboard=True)
        )
    else:
        await message.answer("Некоректний ввід")


@dp.message_handler(state=StateMessage.check)
async def set_message(message: types.Message, state: FSMContext):
    if message.text == "Відправити":
        data = await state.get_data()
        await state.finish()
        await spam_all_groups(data, message)
    else:
        await message.answer("Некоректний ввід")


if __name__ == '__main__':
    executor.start_polling(dispatcher=dp, skip_updates=True)
