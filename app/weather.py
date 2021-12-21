import os
from pathlib import Path
from dotenv import load_dotenv
import requests
import pprint
import json

## Env
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

class Weather():

    def get_clima(ciudad):
        try:
            response = requests.get(
                'http://api.openweathermap.org/data/2.5/weather', 
                params = {
                    'q': ciudad,
                    'appid': os.environ['WEATHER_TOKEN'],
                    'lang': 'es',
                    'units': 'metric'
                }
            )
            pp = pprint.PrettyPrinter(indent=4)
            pp.pprint(json.loads(response.text))

            return json.loads(response.text)
        except Exception as e:
            print(e)

# a = Weather
# print(a.get_clima('Buenos Aires'))