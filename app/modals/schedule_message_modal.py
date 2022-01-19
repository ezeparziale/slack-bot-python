import json
from typing import Optional
from utils.utils import date, time_minutes_later

def build_modal_view(message: Optional[dict], tz_offset: int):
    modal = {
        "type": "modal",
        "callback_id": "schedule_new_message",
        "submit": {"type": "plain_text", "text": "Aceptar"},
        "close": {"type": "plain_text", "text": "Cancelar"},
        "title": {"type": "plain_text", "text": "Programar mensaje"},
        "private_metadata": json.dumps(message) if message is not None else "",
    }

    blocks = []
    blocks.extend(
        [ 
            {
                "type": "input",
                "block_id": "message",
                "label": {"type": "plain_text", "text": "Descripción"},
                "element": {
                    "type": "plain_text_input",
                    "action_id": "input",
                    "multiline": True,
                },
            },
            {
                "type": "input",
                "block_id": "date",
                "label": {"type": "plain_text", "text": "Fecha"},
                "element": {
                    "type": "datepicker",
                    "action_id": "input",
                    "initial_date": date(tz_offset, 10),
                    "placeholder": {"type": "plain_text", "text": "Seleccionar fecha"},
                },
            },
            {
                "type": "input",
                "block_id": "time",
                "label": {"type": "plain_text", "text": "Hora"},
                "element": {
                    "type": "timepicker",
                    "action_id": "input",
                    "initial_time": time_minutes_later(tz_offset, 10),
                    "placeholder": {"type": "plain_text", "text": "Seleccionar hora"},
                },
            },
        ]
    )
    modal["blocks"] = blocks
    return modal
