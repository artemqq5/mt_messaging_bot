from aiogram.types import ReplyKeyboardRemove
from database import MyDataBase


class ChatRep(MyDataBase):
    async def add_chat(self, message, title, datetime):
        result = self._add_chat(message.chat.id, title, datetime)
        if result is not None:
            await message.answer("Група щойно була додана", reply_markup=ReplyKeyboardRemove())
        else:
            await message.answer("Група була додана ще до цього", reply_markup=ReplyKeyboardRemove())

    async def update_creo(self, message, available):
        result = self._update_chat_creo(message.chat.id, available)
        if result:
            await message.answer(f"Статус оновленно на {available}", reply_markup=ReplyKeyboardRemove())

    async def update_google(self, message, available):
        result = self._update_chat_google(message.chat.id, available)
        if result:
            await message.answer(f"Статус оновленно на {available}", reply_markup=ReplyKeyboardRemove())

    async def update_fb(self, message, available):
        result = self._update_chat_fb(message.chat.id, available)
        if result:
            await message.answer(f"Статус оновленно на {available}", reply_markup=ReplyKeyboardRemove())

    async def update_console(self, message, available):
        result = self._update_chat_console(message.chat.id, available)
        if result:
            await message.answer(f"Статус оновленно на {available}", reply_markup=ReplyKeyboardRemove())

    async def update_agency(self, message, available):
        result = self._update_chat_agency(message.chat.id, available)
        if result:
            await message.answer(f"Статус оновленно на {available}", reply_markup=ReplyKeyboardRemove())

    async def update_apps(self, message, available):
        result = self._update_chat_apps(message.chat.id, available)
        if result:
            await message.answer(f"Статус оновленно на {available}", reply_markup=ReplyKeyboardRemove())

    async def update_pp_web(self, message, available):
        result = self._update_chat_pp_web(message.chat.id, available)
        if result:
            await message.answer(f"Статус оновленно на {available}", reply_markup=ReplyKeyboardRemove())

    async def update_pp_ads(self, message, available):
        result = self._update_chat_pp_ads(message.chat.id, available)
        if result:
            await message.answer(f"Статус оновленно на {available}", reply_markup=ReplyKeyboardRemove())

    async def update_media(self, message, available):
        result = self._update_chat_media(message.chat.id, available)
        if result:
            await message.answer(f"Статус оновленно на {available}", reply_markup=ReplyKeyboardRemove())
