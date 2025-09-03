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

        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    def get_by_username(self, username: str, offset=0, limit=None):
        query = 'SELECT * FROM logs WHERE username = ? ORDER BY timestamp DESC'
        params = [username]

        if limit is not None:
            query += ' LIMIT ? OFFSET ?'
            params.extend([limit, offset])

        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    def get_all_usernames(self, offset=0, limit=None):
        query = 'SELECT DISTINCT username FROM logs'
        params = []

        if limit is not None:
            query += ' LIMIT ? OFFSET ?'
            params.extend([limit, offset])

        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            return [row[0] for row in cursor.fetchall()]

    def get_all_machines(self, offset=0, limit=None):
        query = 'SELECT DISTINCT machine FROM logs'
        params = []

        if limit is not None:
            query += ' LIMIT ? OFFSET ?'
            params.extend([limit, offset])

        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            return [row[0] for row in cursor.fetchall()]

    def get_by_machine(self, machine: str, offset=0, limit=None):
        query = 'SELECT * FROM logs WHERE machine = ? ORDER BY timestamp DESC'
        params = [machine]

        if limit is not None:
            query += ' LIMIT ? OFFSET ?'
            params.extend([limit, offset])

        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    def get_by_date_range(self, start_date: str, end_date: str, offset=0, limit=None):
        query = 'SELECT * FROM logs WHERE DATE(timestamp) BETWEEN DATE(?) AND DATE(?) ORDER BY timestamp DESC'
        params = [start_date, end_date]

        if limit is not None:
            query += ' LIMIT ? OFFSET ?'
            params.extend([limit, offset])

        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    def search_text(self, query: str, offset=0, limit=None):
        sql_query = 'SELECT * FROM logs WHERE keylog LIKE ? ORDER BY timestamp DESC'
        params = [f'%{query}%']

        if limit is not None:
            sql_query += ' LIMIT ? OFFSET ?'
            params.extend([limit, offset])

        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute(sql_query, params)
            return [dict(row) for row in cursor.fetchall()]

    def delete_log(self, log_id: int):
        self.cursor.execute('DELETE FROM logs WHERE id = ?', (log_id,))
        self.conn.commit()

    def close(self):
        self.conn.close()

    def fetch_logs_filtered(self, username=None, machine=None, start_date=None, end_date=None, search_query=None, offset=0, limit=None):
        query = 'SELECT * FROM logs WHERE 1=1'
        params = []
        
        if username:
            query += ' AND username = ?'
            params.append(username)
        
        if machine:
            query += ' AND machine = ?'
            params.append(machine)
        
        if start_date and end_date:
            query += ' AND datetime(timestamp) BETWEEN datetime(?) AND datetime(?)'
            params.extend([start_date, end_date])
        
        if search_query:
            query += ' AND keylog LIKE ?'
            params.append(f'%{search_query}%')
        
        query += ' ORDER BY timestamp DESC'
        
        if limit is not None:
            query += ' LIMIT ? OFFSET ?'
            params.extend([limit, offset])
        
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

