from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode, ReplyKeyboardMarkup, KeyboardButton, BotCommand, ReplyKeyboardRemove
from aiogram.utils import executor

from config.cfg import BOT_TOKEN_ID
from database import MyDataBase
from keyboard.chat_ import chat_type_category
from notify.message_spam import spam_all_groups
from repository.chat_rep import ChatRep
# from notify.message_spam import spam_all_groups
from role.accesses import access_admin_to_chat, TypeOfChats
from states.state_message import StateMessage

storage = MemoryStorage()
bot = Bot(token=BOT_TOKEN_ID, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=['start'], state='*')
async def welcome(message: types.Message, state: FSMContext):
    # cancel state if not None
    # commands = [
    #     BotCommand(command="start", description="Запустити бота"),
    #     BotCommand(command="messaging", description="Розсилка"),
    #     BotCommand(command="add_agency", description="add agency chat"),
    #     BotCommand(command="add_apps", description="add apps chat"),
    #     BotCommand(command="add_google", description="add google chat"),
    #     BotCommand(command="add_fb", description="add fb chat"),
    #     BotCommand(command="add_console", description="add console chat"),
    #     BotCommand(command="add_creo", description="add creo chat"),
    #     BotCommand(command="add_pp_web", description="add pp web chat"),
    #     BotCommand(command="add_pp_ads", description="add pp ads chat"),
    #     # Add more commands as needed
    # ]
    # await bot.set_my_commands(commands)
    current_state = await state.get_state()
    if current_state is not None:
        await state.reset_state()
        await message.answer("Операцію було скасовано", reply_markup=ReplyKeyboardRemove())
    else:
        if message.chat.type in [types.ChatType.GROUP, types.ChatType.SUPER_GROUP]:
            await ChatRep().add_chat(message, message.chat.title)  # add group to db
        elif message.chat.type in [types.ChatType.PRIVATE, ]:
            if MyDataBase()._is_admin(message['from']['id']) is not None:
                await message.answer("<b>Привіт, це бот для розсилки сповіщень</b>\n\n"
                                     "Щоб додати групу в розсилку, додайте до неї цього бота як адміна та введіть команду /start\n\n"
                                     "Щоб відправити повідомлення всім групам, введіть команду /messaging",
                                     reply_markup=ReplyKeyboardRemove())
            else:
                await message.answer("Зареєструйся спочатку", reply_markup=ReplyKeyboardRemove())


@dp.message_handler(commands=['add_agency', 'add_apps', 'add_google', 'add_fb', 'add_console', 'add_creo', 'add_pp_web',
                              'add_pp_ads'])
async def add(message: types.Message):
    if MyDataBase()._is_admin(message['from']['id']) is not None:
        if message.chat.type in [types.ChatType.GROUP, types.ChatType.SUPER_GROUP]:

            available = 0
            try:
                text = int(message.text.split(' ')[1])
                if text in (0, 1):
                    available = text
            except Exception as e:
                print(f"exception add {e}")

            if message.text.startswith("/add_agency"):
                await ChatRep().update_agency(message, available)
            elif message.text.startswith("/add_apps"):
                await ChatRep().update_apps(message, available)
            elif message.text.startswith("/add_google"):
                await ChatRep().update_google(message, available)
            elif message.text.startswith("/add_fb"):
                await ChatRep().update_fb(message, available)
            elif message.text.startswith("/add_console"):
                await ChatRep().update_console(message, available)
            elif message.text.startswith("/add_creo"):
                await ChatRep().update_creo(message, available)
            elif message.text.startswith("/add_pp_web"):
                await ChatRep().update_pp_web(message, available)
            elif message.text.startswith("/add_pp_ads"):
                await ChatRep().update_pp_ads(message, available)

    else:
        await message.answer("Зареєструйся спочатку", reply_markup=ReplyKeyboardRemove())


@dp.message_handler(commands=['messaging'])
async def send_messeging_to_all(message: types.Message):
    if message.chat.type in [types.ChatType.PRIVATE, ]:
        admin = MyDataBase()._is_admin(message.chat.id)
        if admin is not None:
            await StateMessage.category.set()
            await message.answer("Оберіть тип чату для відправки: ", reply_markup=chat_type_category(admin))
        else:
            await message.answer("Відмовлено в доступі", reply_markup=ReplyKeyboardRemove())


@dp.message_handler(state=StateMessage.category)
async def set_category(message: types.Message, state: FSMContext):
    admin = MyDataBase()._is_admin(message.chat.id)
    if admin is None or message.text in access_admin_to_chat[admin['role']]:
        await state.update_data(category=message.text)
        await StateMessage().message.set()
        await message.answer(
            "Введіть свій текст для розсилки: ",
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        await state.reset_state()
        await message.answer("Відмовлено в доступі", reply_markup=ReplyKeyboardRemove())


@dp.message_handler(state=StateMessage.message)
async def set_message(message: types.Message, state: FSMContext):
    await state.update_data(message=message.text)
    await StateMessage.photo.set()
    await message.answer(
        "Відправте фото (саме формат фото, а не файл), якщо потрібно",
        reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton("Пропустити")]], resize_keyboard=True)
    )


@dp.message_handler(content_types=['photo', 'text'], state=StateMessage.photo)
async def set_photo(message: types.Message, state: FSMContext):
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
async def send_message(message: types.Message, state: FSMContext):
    if message.text == "Відправити":
        data = await state.get_data()
        await state.finish()
        await spam_all_groups(data, message, data.get('category', None))
    else:
        await message.answer("Некоректний ввід")


if __name__ == '__main__':
    executor.start_polling(dispatcher=dp, skip_updates=True)

# commands = [
#     BotCommand(command="start", description="Запустити бота"),
#     BotCommand(command="messaging", description="Розсилка"),
#     BotCommand(command="add_agency", description="add agency chat"),
#     BotCommand(command="add_apps", description="add apps chat"),
#     BotCommand(command="add_google", description="add google chat"),
#     BotCommand(command="add_fb", description="add fb chat"),
#     BotCommand(command="add_console", description="add console chat"),
#     BotCommand(command="add_creo", description="add creo chat"),
#     BotCommand(command="add_pp", description="add pp chat"),
#     # Add more commands as needed
# ]
# await bot.set_my_commands(commands)
