from flask import Flask
from slack_bolt import App
from utils.message_blocks import MessageBlocks
from functions.weather import Weather

def register_listener(app: App, flask_app: Flask):

    @app.command("/clima")
    def slash_get_clima(ack, body, client):
        ack()

        text = body.get("text")
        clima = Weather.get_clima(text)
        block_message = MessageBlocks.get_weather_block(clima)
        user_id = body.get("user_id")

        client.chat_postMessage(text=f"Clima", blocks=block_message, channel=user_id)
