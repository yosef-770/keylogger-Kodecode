def key_by_minute(list_on_key):
    details_keys = {}

    for on_minute in list_on_key:
        for timestamp, key in on_minute.items():
            if timestamp in details_keys:
                details_keys[timestamp] += key
            else:
                details_keys[timestamp] = key
    return[{k:v} for k, v in details_keys.items()]


