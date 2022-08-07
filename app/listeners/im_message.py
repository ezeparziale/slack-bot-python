from datetime import datetime
from flask import Flask
from slack_bolt import App, BoltContext
from slack_sdk import WebClient
from app.utils.utils import ts_to_date
from app.models import Message, User
from app.listeners.middleware import no_bot_messages, im_messages
from app import db

def register_listener(app: App, flask_app: Flask):
    
    @app.event("message", middleware=[no_bot_messages, im_messages])
    def message_hello(message, say, client: WebClient, context: BoltContext):
        thread_ts = message.get("thread_ts", message.get("ts"))

        # say("Hola!!!", thread_ts=thread_ts)  # Responde en thread
        say("Hola en direct!!!")  # Responde en thread

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
        db.session.add(message_user)
        db.session.commit()

        user_info = client.users_info(token=context.user_token, user=context.user_id)
        user_data = {
            "id": message.get("user"),
            "user": user_info["user"]["name"],
            "channel": message.get("channel"),
            "last_message": datetime.utcnow(),
        }

        user = User(**user_data)
        db.session.merge(user)
        db.session.commit()
