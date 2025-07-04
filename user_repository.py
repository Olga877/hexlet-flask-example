import psycopg2
from psycopg2.extras import DictCursor

conn = psycopg2.connect("dbname=hexlet user=olga877")

class UserRepository():
    def __init__(self, conn):
        self.conn = conn

    def get_content(self):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("SELECT * FROM users")
            return [dict(row) for row in cur]

    def find(self, id):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("SELECT * FROM users WHERE id = %s", (id,))
            row = cur.fetchone()
            return dict(row) if row else None

    def get_by_term(self, search_term=""):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(
                """
                    SELECT * FROM users
                    WHERE name ILIKE %s OR email ILIKE %s
                """,
                (f"%{search_term}%", f"%{search_term}%"),
            )
            return cur.fetchall()

    def save(self, user):
        if "id" in user and user["id"]:
            self._update(user)
        else:
            self._create(user)

    def _update(self, user):
        with self.conn.cursor() as cur:
            cur.execute(
                "UPDATE users SET name = %s, email = %s WHERE id = %s",
                (user["name"], user["email"], user["id"]),
            )
        self.conn.commit()

    def _create(self, user):
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO users (name, email) VALUES (%s, %s) RETURNING id",
                (user["name"], user["email"]),
            )
            id = cur.fetchone()[0]
            user["id"] = id
        self.conn.commit()
