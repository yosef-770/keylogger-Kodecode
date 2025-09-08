from backend.config import Config
from backend.data.event_repository import EventRepository
from backend.data.machine_repository import MachineRepository


class DatabaseManager:
    def __init__(self,  db_name='logs.db'):
        self.machine_repo = MachineRepository(db_name=db_name)
        self.event_repo = EventRepository(db_name=db_name)

database_manager = DatabaseManager(Config.DQLITE_PATH)