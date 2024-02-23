from aiogram.types import ReplyKeyboardRemove
from database import MyDataBase


class ChatRep(MyDataBase):
    async def add_chat(self, message, title, datetime, link):
        result = self._add_chat(message.chat.id, title, datetime, link)
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

    def update_group_id(self, old_group_id, new_group_id):
        return self._update_group_id(old_group_id, new_group_id)

    def all_chats(self):
        return self._all_chats()

    def chat_by_type(self, chat_type):
        return self._chat_by_type(chat_type)

    def update_chat_link(self, group_id, link):
        return self._update_chat_link(group_id, link)

    def remove_chat(self, group_id):
        return self._remove_chat(group_id)

    def get_chat(self, group_id):
        return self._get_chat(group_id)
