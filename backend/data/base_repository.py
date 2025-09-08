import abc
import sqlite3


class BaseRepository:
    conn = None
    cursor = None

    def __init__(self, db_name='logs.db'):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self._create_table()

    @abc.abstractmethod
    def _create_table(self):
        """Implement in children"""
        pass
