from datetime import datetime

from sqlalchemy import BOOLEAN, FLOAT, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP, DateTime

from app import db


class Message(db.Model):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    user: Mapped[str] = mapped_column(String(80), nullable=False)
    message: Mapped[str] = mapped_column(String(120), nullable=False)
    channel: Mapped[str] = mapped_column(String(120), nullable=False)
    channel_type: Mapped[str] = mapped_column(String(120), nullable=False)
    ts: Mapped[float] = mapped_column(FLOAT, nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    thread: Mapped[bool] = mapped_column(BOOLEAN, nullable=False)


class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(String(80), nullable=False, primary_key=True)
    user: Mapped[str] = mapped_column(String(80), nullable=False)
    channel: Mapped[str] = mapped_column(String(120), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False
    )
    last_message: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False
    )


class Scheduled(db.Model):
    __tablename__ = "scheduled_messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    scheduled_message_id: Mapped[str] = mapped_column(String(120), nullable=False)
    channel: Mapped[str] = mapped_column(String(120), nullable=False)
    text: Mapped[str] = mapped_column(String(120), nullable=False)
    post_at: Mapped[float] = mapped_column(FLOAT, nullable=False)
