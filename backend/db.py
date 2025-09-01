import sqlite3
from typing import List


class DB:
    conn = None
    cursor = None

    def __init__(self, db_name='logs.db'):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                keylog TEXT NOT NULL,
                username TEXT NOT NULL,
                machine TEXT NOT NULL DEFAULT 'unknown'
            )
        ''')
        self.conn.commit()

    def insert_log(self, timestamp, events: List[str], username: str, machine: str):
        keylog = ''.join(events)
        self.cursor.execute('''
            INSERT INTO logs (timestamp, keylog, username, machine)
            VALUES (?, ?, ?, ?)
        ''', (timestamp, keylog, username, machine))
        self.conn.commit()

    def fetch_logs(self, offset=0, limit=None):
        query = 'SELECT * FROM logs ORDER BY timestamp DESC'
        params = []

        if limit is not None:
            query += ' LIMIT ? OFFSET ?'
            params.extend([limit, offset])

        self.cursor.execute(query, params)
        return [dict(row) for row in self.cursor.fetchall()]

    def get_by_username(self, username: str):
        self.cursor.execute('SELECT * FROM logs WHERE username = ? ORDER BY timestamp DESC', (username,))
        return [dict(row) for row in self.cursor.fetchall()]

    def get_all_usernames(self):
        self.cursor.execute('SELECT DISTINCT username FROM logs')
        return [dict(row[0]) for row in self.cursor.fetchall()]

    def get_all_machines(self):
        self.cursor.execute('SELECT DISTINCT machine FROM logs')
        return [dict(row[0]) for row in self.cursor.fetchall()]

    def get_by_machine(self, machine: str):
        self.cursor.execute('SELECT * FROM logs WHERE machine = ? ORDER BY timestamp DESC', (machine,))
        return [dict(row) for row in self.cursor.fetchall()]

    def get_by_date_range(self, start_date: str, end_date: str):
        self.cursor.execute('''
            SELECT * FROM logs 
            WHERE DATE(timestamp) BETWEEN DATE(?) AND DATE(?) 
            ORDER BY timestamp DESC
        ''', (start_date, end_date))
        return [dict(row) for row in self.cursor.fetchall()]

    def search_text(self, query: str):
        self.cursor.execute('SELECT * FROM logs WHERE keylog LIKE ? ORDER BY timestamp DESC', (f'%{query}%',))
        return [dict(row) for row in self.cursor.fetchall()]

    def delete_log(self, log_id: int):
        self.cursor.execute('DELETE FROM logs WHERE id = ?', (log_id,))
        self.conn.commit()

    def close(self):
        self.conn.close()

