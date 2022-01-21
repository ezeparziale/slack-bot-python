import json


class MessageBlocks:
    START_TEXT = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": ("Bienvenido! 👋 \n\n" "*Tengo muchas funciones para ayudarte!*"),
        },
    }

    DIVIDER = {"type": "divider"}

    def get_message_block(message):
        return {"type": "section", "text": {"type": "mrkdwn", "text": message}}

    def get_weather_block(weather):
        return [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*{weather['name']} - {weather['weather'][0]['description'].capitalize()}*\nTemperatura: {weather['main']['temp']}C\nTermica: {weather['main']['feels_like']}C\nHumedad: {weather['main']['humidity']}%",
                },
                "accessory": {
                    "type": "image",
                    "image_url": f"http://openweathermap.org/img/wn/{weather['weather'][0]['icon']}@2x.png",
                    "alt_text": f"{weather['weather'][0]['description'].capitalize()}",
                },
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "image",
                        "image_url": "https://api.slack.com/img/blocks/bkb_template_images/tripAgentLocationMarker.png",
                        "alt_text": "Location Pin Icon",
                    },
                    {
                        "type": "plain_text",
                        "emoji": True,
                        "text": f"Location: {weather['sys']['country']}",
                    },
                ],
            },
        ]

    def get_crypto_block(cryptos):
        blocks = []

        for crypto in list(cryptos):
            link = f"*<www.coingecko.com/es/monedas/{crypto['name'].lower()}|{crypto['name'].upper()}>*" 
            blocks.append(
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"{link} \nSimbolo: {crypto['symbol'].upper()} \nPrecio: {crypto['current_price']:,}",
                        },
                        "accessory": {
                            "type": "image",
                            "image_url": crypto['image'],
                            "alt_text": crypto['symbol'],
                        },
                    }
            )
            blocks.append(
                    {
                        "type": "context",
                        "elements": [
                            {
                                "type": "image",
                                "image_url": "https://api.slack.com/img/blocks/bkb_template_images/tripAgentLocationMarker.png",
                                "alt_text": "Pin Icon",
                            },
                            {
                                "type": "plain_text",
                                "emoji": True,
                                "text": f"Actualizado: {crypto['last_updated']}",
                            },
                        ],
                    },
                
            )
        return blocks
