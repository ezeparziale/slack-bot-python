def no_bot_messages(message, next):
    subtype = message.get("subtype")
    if subtype != "bot_message":
        next()


def im_messages(message, next):
    subtype = message.get("channel_type")
    if subtype == "im":
        next()


def channel_messages(message, next):
    subtype = message.get("channel_type")
    if subtype == "channel":
        next()