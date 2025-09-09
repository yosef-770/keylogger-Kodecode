from backend.data.base_repository import BaseRepository


class EventRepository(BaseRepository):

    def _create_table(self):
        cursor = self.get_cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS keystrokes (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          timestamp INTEGER NOT NULL,
          event TEXT NOT NULL,
          machine_id INTEGER,
          FOREIGN KEY(machine_id) REFERENCES machines(id)
        );
        ''')
        self.conn.commit()

    def insert_event(self, timestamp: int, event: str, machine_id: int):
        cursor = self.get_cursor()
        new = cursor.execute('''
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
        WHERE machine_id = ?
        ORDER BY timestamp DESC'''
        
        params = [machine_id]
        
        if limit is not None:
            query += " LIMIT ?"
            params.append(limit)
        if offset:
            query += " OFFSET ?"
            params.append(offset)

        cursor = self.get_cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        print(f"Repository: Found {len(rows)} events for machine {machine_id} (offset={offset}, limit={limit})")
        return [dict(row) for row in rows]

    def get_count_by_machine_id(self, machine_id: int):
        cursor = self.get_cursor()
        cursor.execute('SELECT COUNT(*) FROM keystrokes WHERE machine_id = ?', (machine_id,))
        result = cursor.fetchone()
        count = dict(result)
        return list(count.values())[0]

