from flask import Flask
from slack_bolt import App, BoltContext
from slack_sdk import WebClient

from app import db
from app.listeners.middleware import channel_messages, no_bot_messages
from app.models import Message, User
from app.utils.utils import ts_to_date


def register_listener(app: App, flask_app: Flask):
    @app.event("message", middleware=[no_bot_messages, channel_messages])
    def message_hello(message, say, client: WebClient, context: BoltContext):
        thread_ts = message.get("thread_ts", message.get("ts"))

        # say("Hola!!!", thread_ts=thread_ts)  # Responde en thread
        say("Hola en canal!!!")  # Responde en thread

        message = {
            "user": message.get("user"),
            "message": message.get("text"),
            "channel": message.get("channel"),
            "channel_type": message.get("channel_type"),
            "ts": float(message.get("thread_ts", message.get("ts"))),
            "date": ts_to_date(float(message.get("thread_ts", message.get("ts")))),
            "thread": True if message.get("thread_ts", False) else False,
        }

        message_user = Message(**message)
        with flask_app.app_context():
            db.session.add(message_user)
            db.session.commit()
