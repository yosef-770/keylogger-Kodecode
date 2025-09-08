from backend.data.base_repository import BaseRepository


class EventRepository(BaseRepository):

    def _create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS keystrokes (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          timestamp INTEGER NOT NULL,
          event TEXT NOT NULL,
          machine_id INTEGER,
          FOREIGN KEY(machine_id) REFERENCES machines(id)
        );
        ''')
        self.conn.commit()

    def insert_event(self, timestamp: int, event: str, machine_id: int):
        new = self.cursor.execute('''
        INSERT INTO keystrokes
        (timestamp, event, machine_id)
        VALUES (?, ?, ?)
        ''', (timestamp, event, machine_id))
        self.conn.commit()
        return new.lastrowid

    def get_events_by_machine_id(self,
                                 machine_id: int,
                                 offset=0,
                                 limit=None):
        query = '''
        SELECT * FROM keystrokes
        WHERE machine_id = ?'''

        self.cursor.execute(query, (machine_id,))
        rows = self.cursor.fetchall()
        return [dict(row) for row in rows]

    def get_count_by_machine_id(self, machine_id: int):
        self.cursor.execute('SELECT COUNT(*) FROM keystrokes WHERE machine_id = ?', (machine_id,))
        return list(dict(self.cursor.fetchone()).values())[0]

