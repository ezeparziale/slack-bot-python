import requests
import pprint
import json
from config import settings


class Weather:
    def get_clima(ciudad):
        try:
            response = requests.get(
                "http://api.openweathermap.org/data/2.5/weather",
                params={
                    "q": ciudad,
                    "appid": settings.weather_token,
                    "lang": "es",
                    "units": "metric",
                },
            )

            return json.loads(response.text)
        except Exception as e:
            print(e)
