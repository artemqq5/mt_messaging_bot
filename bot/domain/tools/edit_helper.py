from aiogram.types import CallbackQuery, InlineKeyboardMarkup


async def edit_or_answer(callback: CallbackQuery, text: str, reply_markup: InlineKeyboardMarkup | None = None):
    try:
        await callback.message.edit_text(text, reply_markup=reply_markup)
    except Exception:
        await callback.message.answer(text, reply_markup=reply_markup)
