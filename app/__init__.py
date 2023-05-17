from logging.config import dictConfig

from flask import Flask, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler

from app.config import settings

dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] [%(levelname)s] [%(module)s] %(message)s",
                "datefmt": "%Y-%m-%d %I:%M:%S %z",
            }
        },
        "handlers": {
            "wsgi": {
                "class": "logging.StreamHandler",
                "stream": "ext://flask.logging.wsgi_errors_stream",
                "formatter": "default",
            }
        },
        "root": {"level": "INFO", "handlers": ["wsgi"]},
    }
)

# SlackBot
slack_client = App(
    token=settings.SLACK_BOT_TOKEN, signing_secret=settings.SLACK_SIGNING_SECRET
)
handler = SlackRequestHandler(slack_client)

# Flask app
app = Flask(__name__)
app.config.from_object(settings)

## SQLAlchemy
db = SQLAlchemy(app)

# CORS
CORS(app)


# Events
@app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)


@app.route("/clima", methods=["POST"])
def slack_slash_clima():
    return handler.handle(request)


@app.route("/schedule_message", methods=["POST"])
def slack_slash_test():
    return handler.handle(request)


## Listeners
from app.listeners import (
    channel_message,
    home,
    im_message,
    mentions,
    reaction,
    schedule,
    weather,
)

home.register_listener(slack_client, app)
reaction.register_listener(slack_client, app)
im_message.register_listener(slack_client, app)
channel_message.register_listener(slack_client, app)
weather.register_listener(slack_client, app)
schedule.register_listener(slack_client, app)
mentions.register_listener(slack_client, app)


if __name__ == "__main__":
    app.run(debug=True)
