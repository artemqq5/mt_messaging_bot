from sqlalchemy import Boolean, DateTime, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class UserModel(Base):
    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint("user_id", "group_id", name="user_group_unique"),
    )

    user_id: Mapped[str] = mapped_column(String(255), primary_key=True)
    username: Mapped[str] = mapped_column(String(255), nullable=True)
    group_id: Mapped[str] = mapped_column(String(255), nullable=False)
    time: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    first_name: Mapped[str] = mapped_column(Text, nullable=True)
    language_code: Mapped[str] = mapped_column(String(100), nullable=True)
    title_group: Mapped[str] = mapped_column("title_gruop", Text, nullable=True)
    link_group: Mapped[str] = mapped_column(Text, nullable=True)


class ChatModel(Base):
    __tablename__ = "chats"

    group_id: Mapped[str] = mapped_column(String(255), primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=True)
    creo: Mapped[bool] = mapped_column(Boolean, default=False, server_default="0")
    shop_google: Mapped[bool] = mapped_column(Boolean, default=False, server_default="0")
    shop_fb: Mapped[bool] = mapped_column(Boolean, default=False, server_default="0")
    console: Mapped[bool] = mapped_column(Boolean, default=False, server_default="0")
    apps: Mapped[bool] = mapped_column(Boolean, default=False, server_default="0")
    affiliate_mp: Mapped[bool] = mapped_column(Boolean, default=False, server_default="0")
    partner_mp: Mapped[bool] = mapped_column(Boolean, default=False, server_default="0")
    media_mt: Mapped[bool] = mapped_column(Boolean, default=False, server_default="0")
    agency_google: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="0")
    agency_fb: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="0")
    media_mp: Mapped[bool] = mapped_column(Boolean, default=False, server_default="0")
    partner_mt: Mapped[bool] = mapped_column(Boolean, default=False, server_default="0")
    time: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    link: Mapped[str] = mapped_column(Text, nullable=True)


class AdminModel(Base):
    __tablename__ = "admins"

    telegram_id: Mapped[str] = mapped_column(String(255), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=True)
    role: Mapped[str] = mapped_column(String(255), nullable=True, default="ADMIN", server_default="ADMIN")


class BroadcastModel(Base):
    __tablename__ = "broadcasts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    admin_id: Mapped[str] = mapped_column(String(255), nullable=False)
    admin_name: Mapped[str] = mapped_column(String(255), nullable=True)
    category: Mapped[str] = mapped_column(String(255), nullable=False)
    message_text: Mapped[str] = mapped_column(Text, nullable=True)
    has_photo: Mapped[bool] = mapped_column(Boolean, default=False, server_default="0")
    has_buttons: Mapped[bool] = mapped_column(Boolean, default=False, server_default="0")
    sent_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    groups_count: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
