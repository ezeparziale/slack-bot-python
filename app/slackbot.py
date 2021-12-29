from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
import pprint
from message_blocks import MessageBlocks
from flask import request
from weather import Weather


class SlackBot:
    def __init__(self, SLACK_BOT_TOKEN, SLACK_SIGNING_SECRET, flask_app) -> None:
        ## Slack client
        self.slack_client = App(
            token=SLACK_BOT_TOKEN, signing_secret=SLACK_SIGNING_SECRET
        )

        ## Slack events
        self.handler = SlackRequestHandler(self.slack_client)

        ## Flask app
        self.flask_app = flask_app

        ## Events

        @self.slack_client.event("message")
        def message_hello(message, say):
            # pp = pprint.PrettyPrinter(indent=4)
            # pp.pprint(message)
            thread_ts = message.get("thread_ts", message.get("ts"))
            say("hellow", thread_ts=thread_ts)

        @self.slack_client.event("reaction_added")
        def reaction_message(body, say):
            # pp = pprint.PrettyPrinter(indent=4)
            # pp.pprint(body)
            thread_ts = body.get("event").get("event_ts")
            say("OK!", thread_ts=thread_ts)

        @self.slack_client.command("/clima")
        def slash_get_clima(ack, body):
            # pp = pprint.PrettyPrinter(indent=4)
            # pp.pprint(body)
            text = body.get("text")
            clima = Weather.get_clima(text)
            block_message = MessageBlocks.get_weather_block(clima)
            ack(text=f"", blocks=block_message)

        @self.flask_app.route("/slack/events", methods=["POST"])
        def slack_events():
            return self.handler.handle(request)

        @self.flask_app.route("/clima", methods=["POST"])
        def slack_slash_clima():
            return self.handler.handle(request)
