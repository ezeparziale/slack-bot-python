from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.sqltypes import FLOAT, Boolean, DateTime, TIMESTAMP
from sqlalchemy.sql.expression import text
from database import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, nullable=False)
    user = Column(String(80), nullable=False)
    message = Column(String(120), nullable=False)
    channel = Column(String(120), nullable=False)
    channel_type = Column(String(120), nullable=False)
    ts = Column(FLOAT, nullable=False)
    date = Column(DateTime, nullable=False)
    thread = Column(Boolean, nullable=False)


class User(Base):
    __tablename__ = "users"

    id = Column(String(80), nullable=False, primary_key=True)
    user = Column(String(80), nullable=False)
    channel = Column(String(120), nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False
    )
    last_message = Column(
        TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False
    )


class Scheduled(Base):
    __tablename__ = "scheduled_messages"

    id = Column(Integer, primary_key=True, nullable=False)
    scheduled_message_id = Column(String(120), nullable=False)
    channel = Column(String(120), nullable=False)
    text = Column(String(120), nullable=False)
    post_at = Column(FLOAT, nullable=False)
