from app import db
from sqlalchemy import Column, Integer, String, FLOAT, BOOLEAN
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import DateTime, TIMESTAMP


class Message(db.Model):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, nullable=False)
    user = Column(String(80), nullable=False)
    message = Column(String(120), nullable=False)
    channel = Column(String(120), nullable=False)
    channel_type = Column(String(120), nullable=False)
    ts = Column(FLOAT, nullable=False)
    date = Column(DateTime, nullable=False)
    thread = Column(BOOLEAN, nullable=False)


class User(db.Model):
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


class Scheduled(db.Model):
    __tablename__ = "scheduled_messages"

    id = Column(Integer, primary_key=True, nullable=False)
    scheduled_message_id = Column(String(120), nullable=False)
    channel = Column(String(120), nullable=False)
    text = Column(String(120), nullable=False)
    post_at = Column(FLOAT, nullable=False)
