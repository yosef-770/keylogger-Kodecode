from getpass import getuser

import requests


def send_logs_to_backend(list_minute_of_keys):
    username = getuser()

    for minute in list_minute_of_keys:
        items = list(minute.items())[0]
        print(list(items))
        data = {
            "time": items[0],
            "events": items[1],
            "machine": username,
        }
        # requests.post(consts.API_BASE_URL + "/logs", json=data)