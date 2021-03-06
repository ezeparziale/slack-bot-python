from datetime import datetime
from flask import Flask
from slack_bolt import App, BoltContext
from slack_sdk import WebClient
from utils.utils import ts_to_date
from models import Message, User
from listeners.middleware import no_bot_messages, im_messages


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
        flask_app.session.add(message_user)
        flask_app.session.commit()

        user_info = client.users_info(token=context.user_token, user=context.user_id)
        user_data = {
            "id": message.get("user"),
            "user": user_info["user"]["name"],
            "channel": message.get("channel"),
            "last_message": datetime.utcnow(),
        }

        user = User(**user_data)
        flask_app.session.merge(user)
        flask_app.session.commit()
