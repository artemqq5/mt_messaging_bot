from datetime import datetime

from aiogram import Router, F, Bot
from aiogram.types import Message

from bot.data.repositories.ChatRepository import ChatRepository
from bot.presentation.keyboard.admin_ import kb_back_to_main

router = Router()


@router.message(F.forward_from_chat)
async def handle_forwarded_group(message: Message, bot: Bot):
    chat = message.forward_from_chat
    if chat.type not in ("group", "supergroup"):
        await message.answer(
            "Це не групове повідомлення. Перешли повідомлення з потрібної групи.",
            reply_markup=kb_back_to_main()
        )
        return

    existing = await ChatRepository.get_chat(chat.id)
    if existing:
        await message.answer(
            f"Група <b>{chat.title}</b> вже є в базі.",
            reply_markup=kb_back_to_main()
        )
        return

    try:
        me = await bot.get_me()
        member = await bot.get_chat_member(chat.id, me.id)
        if member.status not in ("member", "administrator"):
            await message.answer(
                f"Бот не є учасником групи <b>{chat.title}</b>. "
                f"Спочатку додайте бота в групу.",
                reply_markup=kb_back_to_main()
            )
            return
    except Exception:
        await message.answer(
            f"Не вдалося перевірити групу <b>{chat.title}</b>. "
            f"Переконайтесь, що бот доданий туди.",
            reply_markup=kb_back_to_main()
        )
        return

    new_chat = await ChatRepository.add_chat(
        group_id=chat.id,
        title=chat.title,
        datetime=datetime.now()
    )
    if new_chat:
        try:
            chat_info = await bot.get_chat(chat.id)
            if chat_info.invite_link:
                await ChatRepository.update_chat_link(chat.id, chat_info.invite_link)
        except Exception:
            pass
        await message.answer(
            f"✅ Група <b>{chat.title}</b> (<code>{chat.id}</code>) додана до бази!\n\n"
            f"Категорії ще не призначені. Відкрийте групу через «📋 Переглянути групи» → "
            f"«⚙️ Налаштування», щоб увімкнути потрібні категорії.",
            reply_markup=kb_back_to_main()
        )
    else:
        await message.answer(
            "❌ Помилка при додаванні групи.",
            reply_markup=kb_back_to_main()
        )
