import sqlite3

from backend.config import Config


class DB:
    conn = None
    cursor = None

    def __init__(self, db_name='logs.db'):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS connections (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  status TEXT DEFAULT 'active',
  timestamp INTEGER NOT NULL,
  username TEXT,
  processor TEXT,
  system TEXT,
  node TEXT,
  release TEXT,
  version TEXT,
  machine TEXT,
  ip_address TEXT
);''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  timestmp INTEGER NOT NULL,
  event TEXT NOT NULL,
  connection_id INTEGER,
  FOREIGN KEY(connection_id) REFERENCES connections(id)
);
''')
        self.conn.commit()

    def init_connection(self, timestamp, username, processor, system, node, release, version, machine, ip_address):
        new = self.cursor.execute('''
            INSERT INTO connections (timestamp, username, processor, system, node, release, version, machine, ip_address)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (timestamp, username, processor, system, node, release, version, machine, ip_address))
        self.conn.commit()
        return new.lastrowid

    def close_connection(self, connection_id):
        self.cursor.execute('''
            UPDATE connections
            SET status = 'closed'
            WHERE id = ?
        ''', (connection_id,))
        self.conn.commit()

    def insert_log(self, connection_id: int, timestamp: int, event: str):
        self.cursor.execute('''
            INSERT INTO events (timestmp, event, connection_id)
            VALUES (?, ?, ?)
        ''', (timestamp, str(event), connection_id))
        self.conn.commit()

    def delete_log(self, log_id: int):
        self.cursor.execute('''
            DELETE FROM events
            WHERE id = ?
        ''', (log_id,))
        self.conn.commit()

    def delete_connection(self, connection_id: int):
        self.cursor.execute('''
            DELETE FROM connections
            WHERE id = ?
        ''', (connection_id,))
        self.conn.commit()


    def get_connections(self,
                        status=None,
                        offset=0,
                        limit=None,
                        username=None,
                        machine=None,
                        start_date=None,
                        end_date=None):
        query = "SELECT * FROM connections WHERE 1=1"
        params = []

        if username:
            query += " AND username = ?"
            params.append(username)
        if machine:
            query += " AND machine = ?"
            params.append(machine)
        if start_date:
            query += " AND timestamp >= ?"
            params.append(start_date)
        if end_date:
            query += " AND timestamp <= ?"
            params.append(end_date)

        if status:
            query += " AND status = ?"
            params.append(status)

        query += " ORDER BY timestamp DESC"

        if limit is not None:
            query += " LIMIT ?"
            params.append(limit)
        if offset:
            query += " OFFSET ?"
            params.append(offset)

        self.cursor.execute(query, params)
        rows = self.cursor.fetchall()
        return [dict(row) for row in rows]

    def get_connection_by_id(self, connection_id: int):
        # return the connection and its events count and last event date
        self.cursor.execute('''
            SELECT c.*, 
                   (SELECT COUNT(*) FROM events e WHERE e.connection_id = c.id) AS event_count,
                   (SELECT MAX(timestmp) FROM events e WHERE e.connection_id = c.id) AS last_event_date
            FROM connections c
            WHERE c.id = ?
        ''', (connection_id,))
        row = self.cursor.fetchone()
        return dict(row) if row else None

    def get_events_by_connection(self, connection_id: int, offset=0, limit=None, start_date=None,end_date=None):
        query = "SELECT * FROM events WHERE connection_id = ?"
        params = [connection_id]

        if start_date:
            query += " AND timestmp >= ?"
            params.append(start_date)
        if end_date:
            query += " AND timestmp <= ?"
            params.append(end_date)

        query += " ORDER BY timestmp DESC"

        if limit is not None:
            query += " LIMIT ?"
            params.append(limit)
        if offset:
            query += " OFFSET ?"
            params.append(offset)

        self.cursor.execute(query, params)
        rows = self.cursor.fetchall()
        return [dict(row) for row in rows]

db_manager = DB(Config.DQLITE_PATH)
