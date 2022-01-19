from datetime import datetime
from flask import Flask
from slack_bolt import App, BoltContext, Ack, Respond
from slack_sdk import WebClient
from modals.schedule_message_modal import build_modal_view
from slack_sdk.errors import SlackApiError
from utils.utils import built_post_at, tz_info
from models import Scheduled
from actions.update_home import update_home_tab


def register_listener(app: App, flask_app: Flask):

    @app.action("schedule_new_message_button")
    @app.command("/schedule_message")
    def open_schedule_new_message_modal(
        ack: Ack, body: dict, context: BoltContext, client: WebClient
    ):
        ack()

        user_info = client.users_info(token=context.user_token, user=context.user_id)
        tz_offset = user_info["user"]["tz_offset"]

        client.views_open(
            trigger_id=body["trigger_id"],
            view=build_modal_view(None, tz_offset),
        )


    @app.view("schedule_new_message")
    def schedule_new_message_view_submission(
        body: dict, ack: Ack, context: BoltContext, client: WebClient, event
    ):
        user_info = client.users_info(token=context.user_token, user=context.user_id)
        tz_offset = user_info["user"]["tz_offset"]

        submitted_data = body["view"]["state"]["values"]
        message_text = submitted_data.get("message", {}).get("input", {}).get("value")
        date = submitted_data["date"]["input"]["selected_date"]
        time = submitted_data["time"]["input"]["selected_time"]

        user_id = body.get("user").get("id")
        post_at = built_post_at(tz_offset, date, time)

        message = {
            "text": ":timer_clock: " + message_text,
            "channel": user_id,
            "post_at": post_at.timestamp(),
        }

        errors = {}
        if post_at <= datetime.now(tz=tz_info(tz_offset)):
            fecha_poast_at = post_at.strftime('%Y-%m-%d')
            hora_poast_at = post_at.strftime('%H:%M')
            fecha_hoy = datetime.now(tz=tz_info(tz_offset)).strftime('%Y-%m-%d')
            hora_hoy = datetime.now(tz=tz_info(tz_offset)).strftime('%H:%M')
            if fecha_poast_at < fecha_hoy:
                errors["date"] = "Selecciona una fecha correcta"
            else:
                if hora_poast_at <= hora_hoy:
                    errors["time"] = "Selecciona una hora correcta"

        if len(errors):
            return ack(
                response_action="errors",
                errors=errors,
            )

        try:
            result = client.chat_scheduleMessage(
                token=context.user_token,
                channel=user_id,
                text=message.get("text", ""),
                attachments=message.get("attachments"),
                blocks=message.get("blocks"),
                post_at=message.get("post_at"),
            )

            message = {
                "scheduled_message_id": result.get("scheduled_message_id"),
                "channel": result.get("channel"),
                "post_at": result.get("post_at"),
                "text": result.get("message").get("text"),
            }
            scheduled_message = Scheduled(**message)
            flask_app.session.merge(scheduled_message)
            flask_app.session.commit()

            ack()

            update_home_tab(event, client, context, flask_app)

        except SlackApiError as e:
            print("Error: ", e)
