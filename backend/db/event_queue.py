
from queue import Queue

from backend.db.db import DB


def db_worker(event_queue: Queue, db: DB):
    while True:
        event = event_queue.get()
        if event is None or event.key is None:
            break

        db.insert_log(connection_id=event.connection_id, event=event.key, timestamp=event.timestamp)
        event_queue.task_done()