import logging
from multiprocessing.queues import Queue

from backend.data.database_manager import database_manager


def db_worker(event_queue: Queue):
    while True:
        event = event_queue.get()
        if event is None or event['event'] is None:
            break

        machine = database_manager.machine_repo.get_machine_by_username(event["username"])

        if not machine:
            return

        database_manager.event_repo.insert_event(
            timestamp=event['timestamp'],
            machine_id=machine['id'],
            event=event['event']
        )
