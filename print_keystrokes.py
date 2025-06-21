def print_key_log(list_minute_of_keys):
    for i, minute_of_keys in enumerate(list_minute_of_keys):
        for key, value in minute_of_keys.items():
            if i == len(list_minute_of_keys)-1:
                value = value[:-4]
            print("*****", key, "*****")
            print(value)
