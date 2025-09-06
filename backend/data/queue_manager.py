import queue

from backend.data.repository import db_manager

# Event queue setup
event_queue = queue.Queue()


def db_worker():
    while True:
        event = event_queue.get()
        if event is None or event.key is None:
            break

        db_manager.insert_log(connection_id=event.connection_id, event=event.key, timestamp=event.timestamp)
        event_queue.task_done()