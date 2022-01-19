import models
from datetime import datetime


def update_home_tab(event, client, context, flask_app):
    user_id = context["user_id"]
    try:
        schedule_messages = (
            flask_app.session.query(models.Scheduled)
            .join(models.User, models.Scheduled.channel == models.User.channel, isouter=True)
            .filter(models.User.id == user_id)
            .filter(models.Scheduled.post_at >= datetime.now().timestamp())
            .all()
        )

        user = (
            flask_app.session.query(models.User)
            .filter(models.User.id == user_id)
            .all()
        ) 
    except Exception:
        schedule_messages = []



    blocks = []
    blocks.append(
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": ":wave: *Bienvenido <@" + context["user_id"] + "> :house:*"
            }
        }
    )

    if user:
        blocks.append(
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": "Programar un mensaje :point_right:"},
                "accessory": {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Nuevo",
                    },
                    "value": "edit",
                    "style": "primary",
                    "action_id": "schedule_new_message_button",
                },
            }
        )
    else:
        blocks.append(
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": "Inicializar bot :robot_face:"},
                "accessory": {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": ":wave:",
                    },
                    "value": "edit",
                    "style": "primary",
                    "action_id": "hello_bot",
                },
            }
        )

    # schedule_messages
    for msg in schedule_messages:
        time = datetime.fromtimestamp(msg.post_at)
        blocks.append({"type": "divider"})
        blocks.append(
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"{msg.text}\n\n Programado para: {time}",
                },
                "accessory": {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Eliminar",
                    },
                    "value": f"{msg.channel}_{msg.scheduled_message_id}",
                    "style": "danger",
                    "action_id": "delete_scheduled_message_button",
                },
            }
        )

    client.views_publish(
        user_id=context["user_id"],
        view={
            "type": "home",
            "blocks": blocks
        }
    )
