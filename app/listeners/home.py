from flask import Flask
from slack_bolt import App, BoltContext, Ack
from slack_sdk import WebClient
from models import Scheduled
from actions.update_home import update_home_tab
from models import User
from datetime import datetime


def register_listener(app: App, flask_app: Flask):

    @app.event("app_home_opened")
    def show_home_tab(event, client, context):
        update_home_tab(event, client, context, flask_app)


    @app.action("delete_scheduled_message_button")
    def delete_scheduled_message(
        ack: Ack, action: dict, context: BoltContext, client: WebClient, event
    ):
        channel, scheduled_message_id = action["value"].split("_")

        client.chat_deleteScheduledMessage(
            token=context.user_token,
            channel=channel,
            scheduled_message_id=scheduled_message_id,
        )
        ack()
        user_info = client.users_info(token=context.user_token, user=context.user_id)

        schedule_message = (
            flask_app.session.query(Scheduled)
            .filter(Scheduled.scheduled_message_id == scheduled_message_id)
        )
        schedule_message.delete(synchronize_session=False)
        flask_app.session.commit()

        update_home_tab(event, client, context, flask_app)


    @app.action("hello_bot")
    def init_bot_user(
        ack: Ack, action: dict, context: BoltContext, client: WebClient, event
    ):
        ack()

        user_id = context["user_id"]
        channel_id=""
        response = client.chat_postMessage(text=f"Bienvenido!!! :grinning:\n Ya puedes disfrutar de todas mis funciones :tada:", channel=user_id)

        user_info = client.users_info(token=context.user_token, user=context.user_id)

        user_data = {
            "id": user_id,
            "user": user_info["user"]["name"],
            "channel": response["channel"],
            "last_message": datetime.utcnow(),
        }

        user = User(**user_data)
        flask_app.session.merge(user)
        flask_app.session.commit()

        update_home_tab(event, client, context, flask_app)
