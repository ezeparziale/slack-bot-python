from flask import Flask
from slack_bolt import App
from utils.message_blocks import MessageBlocks
from functions.cryptocurrency import Crypto

def register_listener(app: App, flask_app: Flask):

    @app.command("/crypto")
    def slash_get_crypto(ack, body, client):
        ack()

        text = body.get("text")
        crypto_currency = Crypto.get_crypto_currency(text)
        block_message = MessageBlocks.get_crypto_block(crypto_currency)
        user_id = body.get("user_id")
        print(block_message)
        client.chat_postMessage(text=f"Crypto", blocks=block_message, channel=user_id)
