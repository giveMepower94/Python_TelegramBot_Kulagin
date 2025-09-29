import psycopg2
from secret import HOST, DATABASE, PASSWORD, PORT, USER


class CalendarDB:
    def __init__(
        self,
        host=HOST,
        database=DATABASE,
        user=USER,
        password=PASSWORD,
        port=PORT

    ):
        self.conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port
        )
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            details TEXT
        )
        """)
        self.conn.commit()

    def create_event(self, name, date, time, details):
        self.cursor.execute(
            "INSERT INTO events (name, date, time, details) VALUES (?, ?, ?, ?)",
            (name, date, time, details)
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def read_event(self, event_id):
        self.cursor.execute(
            "SELECT * FROM events WHERE id = ?",
            (event_id,)
        )
        self.conn.commit()
        return self.cursor.fetchone()

    def edit_event(self, event_id, name=None, date=None, time=None, details=None):
        event = self.read_event(event_id)

        if not event:
            False
        name = name or event[1]
        date = date or event[2]
        time = time or event[3]
        details = details or event[4]

        self.cursor.execute(
            "UPDATE events SET name=?, date=?, time=?, details=? WHERE id=?",
            (name, date, time, details, event_id)
        )
        self.conn.commit()
        return True

    def delete_event(self, event_id):
        self.cursor.execute("DELETE FROM events WHERE id=?", (event_id,))
        self.conn.commit()
        return self.cursor.rowcount > 0

    def get_list_event(self, date):
        self.cursor.execute("SELECT * FROM events WHERE date=?", (date,))
        return self.cursor.fetchall()
