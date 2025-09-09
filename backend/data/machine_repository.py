import time

from backend.data.base_repository import BaseRepository


class MachineRepository(BaseRepository):

    def _create_table(self):
        cursor = self.get_cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS machines (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          display_username TEXT NOT NULL,
          active BOOL DEFAULT true,
          first_login INTEGER NOT NULL,
          title TEXT,
          machine_username TEXT,
          mac_address TEXT,
          processor TEXT,
          system TEXT,
          node TEXT,
          release TEXT,
          version TEXT,
          machine TEXT,
          ip_address TEXT
        );''')
        self.conn.commit()

    def create_machine(self, display_username, metadata):
        first_login = time.time()
        cursor = self.get_cursor()
        new = cursor.execute('''
            INSERT INTO machines 
            (display_username, first_login, machine_username, mac_address, processor, system, node, release, version, machine, ip_address)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (display_username, first_login,
              metadata['username'], metadata['mac_address'], metadata['processor'],
              metadata['system'], metadata['node'], metadata['release'],
              metadata['version'], metadata['machine'], metadata['ip_address']))
        self.conn.commit()
        return new.lastrowid

    def get_machine_by_username(self, display_username):
        cursor = self.get_cursor()
        cursor.execute('''
            SELECT * FROM machines 
            WHERE display_username = ?
        ''', (display_username,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def get_machine_by_id(self, machine_id):
        cursor = self.get_cursor()
        cursor.execute('''
            SELECT * FROM machines 
            WHERE id = ?
        ''', (machine_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def set_status(self, username, status: bool):
        cursor = self.get_cursor()
        cursor.execute('''
            UPDATE machines
            SET active = ?
            WHERE display_username = ?
        ''', (status, username))
        self.conn.commit()

    def set_title(self, username, title: str):
        cursor = self.get_cursor()
        cursor.execute('''
            UPDATE machines
            SET title = ?
            WHERE display_username = ?
        ''', (title, username))
        self.conn.commit()

    def get_machines(self,
                     status=None,
                     title=None,
                     offset=0,
                     limit=None,
                     username=None):
        query = "SELECT * FROM machines WHERE 1=1"
        params = []

        if username:
            query += " AND display_username = ?"
            params.append(username)
        if title:
            query += " AND title = ?"
            params.append(title)
        if status:
            query += " AND active = ?"
            params.append(status)

        query += " ORDER BY first_login DESC"

        if limit is not None:
            query += " LIMIT ?"
            params.append(limit)
        if offset:
            query += " OFFSET ?"
            params.append(offset)


        cursor = self.get_cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
