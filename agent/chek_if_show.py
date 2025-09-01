def check_if_get_show(details_keys):
    last_items = details_keys[-4:]
    values = [list(entry.values())[0] for entry in last_items]
    return values == ['s', 'h', 'o', 'w']
