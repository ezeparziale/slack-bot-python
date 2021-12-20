class MessageBlocks():
    START_TEXT = {
        'type': 'section',
        'text': {
            'type': 'mrkdwn',
            'text': (
                'Bienvenido! 👋 \n\n'
                '*Tengo muchas funciones para ayudarte!*'
            )
        }
    }

    DIVIDER = {'type': 'divider'}

    def get_message_block(message):
        return {'type': 'section', 'text': {'type': 'mrkdwn', 'text': message}}
