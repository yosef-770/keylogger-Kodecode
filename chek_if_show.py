def check_if_get_show(details_keys):
    last_items = details_keys[-4:]
    exists = ''.join([list(entry.values())[0] for entry in last_items])

    if 's' in exists and 'h' in exists and 'o' in exists and 'w' in exists:
        return True
    else:
        return False
