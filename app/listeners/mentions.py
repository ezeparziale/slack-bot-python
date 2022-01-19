from flask import Flask
from slack_bolt import App


def register_listener(app: App, flask_app: Flask):
    
    @app.event("app_mention")
    def event_test(body, say, client):
        user = body["event"]["user"]

        client.reactions_add(
                channel=body["event"]["channel"],
                timestamp=body["event"]["ts"],
                name="eyes",
            )


        say(f"Hola!!!{user}")
