def key_by_minute(list_on_key):
    minute_of_keys = {}

    for on_minute in list_on_key:
        for timestamp, key in on_minute.items():
            if timestamp in minute_of_keys:
                minute_of_keys[timestamp] += key
            else:
                minute_of_keys[timestamp] = key
    return[{k:v} for k, v in minute_of_keys.items()]


