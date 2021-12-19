from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask
from slackeventsapi import SlackEventAdapter
import pprint

pp = pprint.PrettyPrinter(indent=4)

## Env
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

## Flask app
app = Flask(__name__)

## Slack events
slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'], '/slack/events/', app)

## Slack client
client = WebClient(token=os.environ['SLACK_TOKEN'])

BOT_ID = client.api_call('auth.test')['user_id']

# Event
@slack_event_adapter.on('message')
def message(payload):
    try:
        pp.pprint(payload)
        event = payload.get('event', {})
        channel_id = event.get('channel')
        user_id = event.get('user')
        text = event.get('text')

        if BOT_ID != user_id:
            client.chat_postMessage(channel=channel_id, text=text)
    except SlackApiError as e:
        assert e.response["ok"] is False
        assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
        print(f"Got an error: {e.response['error']}") 



if __name__ == '__main__':
    app.run(debug=True)