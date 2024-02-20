import datetime

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode, ReplyKeyboardMarkup, KeyboardButton, BotCommand, ReplyKeyboardRemove
from aiogram.utils import executor

from config.cfg import BOT_TOKEN_ID
from database import MyDataBase
from handlers.message_send_handler import register_message_send_handler
from keyboard.chat_ import chat_type_category
from notify.message_spam import spam_all_groups
from notify.send_back_check import send_back_check
from repository.chat_rep import ChatRep
# from notify.message_spam import spam_all_groups
from role.accesses import access_admin_to_chat, TypeOfChats
from states.state_message import StateMessage
from states.state_show_chats import StateShowChats

storage = MemoryStorage()
bot = Bot(token=BOT_TOKEN_ID, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=['start'], state='*')
async def welcome(message: types.Message, state: FSMContext):
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
    #     BotCommand(command="add_media", description="add media chat"),
    #     # Add more commands as needed
    # ]
    # await bot.set_my_commands(commands)

    # cancel state if not None
    current_state = await state.get_state()
    if current_state is not None:
        await state.reset_state()
        await message.answer("Операцію було скасовано", reply_markup=ReplyKeyboardRemove())
    else:
        if message.chat.type in [types.ChatType.GROUP, types.ChatType.SUPER_GROUP]:
            await ChatRep().add_chat(message, message.chat.title, datetime.datetime.now())  # add group to db
        elif message.chat.type in [types.ChatType.PRIVATE, ]:
            if MyDataBase()._is_admin(message['from']['id']) is not None:
                await message.answer("<b>Привіт, це бот для розсилки сповіщень</b>\n\n"
                                     "Щоб додати групу в розсилку, додайте до неї цього бота як адміна та введіть команду /start\n\n"
                                     "Щоб відправити повідомлення всім групам, введіть команду /messaging",
                                     reply_markup=ReplyKeyboardRemove())
            else:
                await message.answer("Зареєструйся спочатку", reply_markup=ReplyKeyboardRemove())


@dp.message_handler(commands=['add_agency', 'add_apps', 'add_google', 'add_fb', 'add_console', 'add_creo', 'add_pp_web',
                              'add_pp_ads', 'add_media'])
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
            elif message.text.startswith("/add_media"):
                await ChatRep().update_media(message, available)
    else:
        await message.answer("Зареєструйся спочатку", reply_markup=ReplyKeyboardRemove())


@dp.message_handler(commands=['messaging'], state='*')
async def send_messeging_to_all(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.reset_state()

    if message.chat.type in [types.ChatType.PRIVATE, ]:
        admin = MyDataBase()._is_admin(message.chat.id)
        if admin is not None:
            await StateMessage.category.set()
            await message.answer("Оберіть тип чату для відправки: ", reply_markup=chat_type_category(admin))
        else:
            await message.answer("Відмовлено в доступі", reply_markup=ReplyKeyboardRemove())


register_message_send_handler(dp)


if __name__ == '__main__':
    executor.start_polling(dispatcher=dp, skip_updates=True)

