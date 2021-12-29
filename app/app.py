import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask
from slackbot import SlackBot

## Env
env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

## Flask app
app = Flask(__name__)

# SlackBot
bot = SlackBot(os.environ["SLACK_BOT_TOKEN"], os.environ["SLACK_SIGNING_SECRET"], app)

if __name__ == "__main__":
    app.run(debug=True)
