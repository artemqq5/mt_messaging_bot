from html import escape

from aiogram import Router, F
from aiogram.types import CallbackQuery

from bot.data.other.accesses import TypeOfAdmins
from bot.data.repositories.AdminRepository import AdminRepository
from bot.data.repositories.ChatRepository import ChatRepository
from bot.data.repositories.UserRepository import UserRepository
from bot.domain.tools.edit_helper import edit_or_answer
from bot.presentation.keyboard.admin_ import MainMenuCallback, kb_back_to_main, CATEGORY_LABELS

router = Router()


@router.callback_query(MainMenuCallback.filter(F.action == "stats"))
async def statistic_info(callback: CallbackQuery):
    admin = await AdminRepository.is_admin(callback.from_user.id)
    if admin is None or admin.role != TypeOfAdmins.ADMIN.value:
        await callback.answer("Немає доступу", show_alert=True)
        return

    chats = await ChatRepository.all_chats() or []
    users_count = await UserRepository.count_users_total() or 0
    admins_list = await AdminRepository.get_all_admins() or []
    cat_counts = await ChatRepository.count_chats_by_category() or {}
    top_groups = await UserRepository.top_groups_by_users(5) or []

    cat_lines = []
    for key, label in CATEGORY_LABELS.items():
        cat_lines.append(f"  {label}: {cat_counts.get(key, 0)}")
    cat_lines.append(f"  Невизначені: {cat_counts.get('unspecified', 0)}")

    top_lines = []
    for i, row in enumerate(top_groups, 1):
        title = escape(str(row.title_group or row.group_id))
        top_lines.append(f"  {i}. {title} — {row.cnt} юзерів")

    info = (
        "<b>Статистика по боту</b>\n\n"
        f"Всього груп: <b>{len(chats)}</b>\n"
        f"Всього юзерів: <b>{users_count}</b>\n"
        f"Всього адмінів: <b>{len(admins_list)}</b>\n\n"
        "<b>Групи по категоріях:</b>\n"
        + "\n".join(cat_lines)
        + ("\n\n<b>Топ-5 груп за юзерами:</b>\n" + "\n".join(top_lines) if top_lines else "")
    )
    await edit_or_answer(callback, info, reply_markup=kb_back_to_main())
    await callback.answer()
