from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slackeventsapi import SlackEventAdapter
import pprint
from message_blocks import MessageBlocks
from flask import request, Response

class SlackBot():

    def __init__(self, SLACK_TOKEN, SIGNING_SECRET, app) -> None:
        ## Slack client
        self.client = WebClient(token=SLACK_TOKEN)
        self.BOT_ID = self.client.api_call('auth.test')['user_id']

        ## Slack events
        self.slack_event_adapter = SlackEventAdapter(SIGNING_SECRET, '/slack/events/', app)

        ## Flask app
        self.app = app

        # Event 
        @self.slack_event_adapter.on('message')
        def message(payload):
            try:
                # pp = pprint.PrettyPrinter(indent=4)
                # pp.pprint(event)
                event = payload.get('event', {})
                channel_id = event.get('channel')
                user_id = event.get('user')
                text = event.get('text')
                ts = event.get('ts')
                message = {
                    'channel': channel_id,
                    'text': 'Message from bot',
                    # 'thread_ts': ts
                }

                if self.BOT_ID != user_id and user_id != None:
                    if text.lower() == 'start':
                        blocks = [ MessageBlocks.START_TEXT ]
                        message.pop('thread_ts')
                    else:
                        blocks = [ MessageBlocks.get_message_block(text) ]
                    message['blocks'] = blocks
                    self.client.chat_postMessage(**message)
            except SlackApiError as e:
                assert e.response["ok"] is False
                assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
                print(f"Got an error: {e.response['error']}")


        @self.slack_event_adapter.on('reaction_added')
        def reaction(payload):
            event = payload.get('event', {})
            item = event.get('item')
            channel_id = item.get('channel')
            user_id = event.get('user')
            ts = item.get('ts')
            reaction = event.get('reaction')
            print('REACIONO')
            pp = pprint.PrettyPrinter(indent=4)
            pp.pprint(event)
            message = {
                'channel': channel_id,
                'text': 'Gracias por la reacción: '+ reaction,
                # 'thread_ts': ts
            }
            self.client.chat_postMessage(**message)


        @self.app.route('/slash-command', methods=['POST'])
        def slash_command():
            print('SLASH')
            data = request.form
            channel_id = data.get('channel_id')
            text = data.get('text')

            # pp = pprint.PrettyPrinter(indent=4)
            # pp.pprint(data)

            message = text

            self.client.chat_postMessage(channel=channel_id, text=f"Message: {message}")
            return Response(), 200

