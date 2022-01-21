from listeners import home, reaction, im_message, channel_message, weather, cryptocurrency, schedule, mentions
from config import settings
from flask import Flask, request, _app_ctx_stack, jsonify, url_for
from flask_cors import CORS
from sqlalchemy.orm import scoped_session
import models
from database import SessionLocal, engine
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler

models.Base.metadata.create_all(bind=engine)

# SlackBot
slack_client = App(token=settings.slack_bot_token, signing_secret=settings.slack_signing_secret)
handler = SlackRequestHandler(slack_client)

## Flask app
app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

CORS(app)
app.session = scoped_session(SessionLocal, scopefunc=_app_ctx_stack.__ident_func__)

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
home.register_listener(slack_client, app)
reaction.register_listener(slack_client, app)
im_message.register_listener(slack_client, app)
channel_message.register_listener(slack_client, app)
weather.register_listener(slack_client, app)
cryptocurrency.register_listener(slack_client, app)
schedule.register_listener(slack_client, app)
mentions.register_listener(slack_client, app)


if __name__ == "__main__":
    app.run(debug=True)
