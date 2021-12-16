import slack
import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

client = slack.WebClient(token=os.environ['SLACK_TOKEN'])

BOT_ID = client.api_call('auth.test')['user_id']

client.chat_postMessage(channel='#test', text='hola')
