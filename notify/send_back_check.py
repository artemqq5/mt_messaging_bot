from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ParseMode


async def send_back_check(message, data):
    if data.get('type_sub_data', None) is None:
        await message.answer(
            data['message'],
            reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton("Відправити")]], resize_keyboard=True)
        )
    elif data.get('type_sub_data', None) == "photo":
        await message.answer_photo(
            data['photo'],
            caption=data['message'],
            reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton("Відправити")]], resize_keyboard=True)
        )
    elif data.get('type_sub_data', None) == "gif":
        await message.answer_document(
            caption=data['message'],
            document=data['gif'],
            reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton("Відправити")]], resize_keyboard=True)
        )
    elif data.get('type_sub_data', None) == "video":
        await message.answer_video(
            caption=data['message'],
            video=data['video'],
            reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton("Відправити")]], resize_keyboard=True)
        )
