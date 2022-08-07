import json

import requests

from app.config import settings


class Crypto:
    def get_crypto_currency(coins):
        try:
            response = requests.get(
                "https://api.coingecko.com/api/v3/coins/markets",
                params={
                    "vs_currency": "usd",
                    "ids": coins,
                    "order": "market_cap_desc",
                    "per_page": "250",
                    "page": "1",
                    "sparkline": False,
                },
            )

            return json.loads(response.text)
        except Exception as e:
            print(e)
