import json

import requests

from app import app
from app.config import settings


class Weather:
    def get_clima(ciudad):
        try:
            response = requests.get(
                "http://api.openweathermap.org/data/2.5/weather",
                params={
                    "q": ciudad,
                    "appid": settings.WEATHER_TOKEN,
                    "lang": "es",
                    "units": "metric",
                },
            )

            return json.loads(response.text)
        except Exception as e:
            app.logger.error(f"Error: {e}")
