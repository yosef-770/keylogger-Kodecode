import abc
import sqlite3
import threading


class BaseRepository:
    def __init__(self, db_name='logs.db'):
        self.db_name = db_name
        self.local = threading.local()
        self._create_table()
    
    def get_connection(self):
        if not hasattr(self.local, 'conn') or self.local.conn is None:
            self.local.conn = sqlite3.connect(self.db_name, check_same_thread=False, timeout=30)
            self.local.conn.row_factory = sqlite3.Row
        return self.local.conn
    
    def get_cursor(self):
        if not hasattr(self.local, 'cursor') or self.local.cursor is None:
            self.local.cursor = self.get_connection().cursor()
        return self.local.cursor

    @property
    def conn(self):
        return self.get_connection()
    
    @property 
    def cursor(self):
        return self.get_cursor()

    @abc.abstractmethod
    def _create_table(self):
        """Implement in children"""
        pass
