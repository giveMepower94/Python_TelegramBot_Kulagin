import psycopg2
from secret import HOST, DATABASE, USER, PASSWORD, PORT


class UsersDB:
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
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                tg_id BIGINT UNIQUE NOT NULL,
                username TEXT,
                first_name TEXT,
                last_name TEXT
            )
        """)
        self.conn.commit()

    def add_user(self, tg_id, username=None, first_name=None, last_name=None):
        self.cursor.execute("""
            INSERT INTO users (tg_id, username, first_name, last_name)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (tg_id) DO NOTHING
            RETURNING id
        """, (tg_id, username, first_name, last_name))

        user_id = self.cursor.fetchone()
        self.conn.commit()
        return user_id[0] if user_id else None

    def get_user(self, tg_id):
        self.cursor.execute("SELECT * FROM users WHERE tg_id = %s", (tg_id,))
        return self.cursor.fetchone()

    def user_exists(self, tg_id):
        self.cursor.execute("SELECT 1 FROM users WHERE tg_id = %s", (tg_id,))
        return bool(self.cursor.fetchone())
