from flask import Flask
from slack_bolt import App


def register_listener(app: App, flask_app: Flask):
    @app.event("reaction_added")
    def reaction_message(say):
        say("Hey! Gracias!")
