import sqlite3
from typing import Optional, List, Any, Union


class DatabaseController:
    database_path = "./resources/database.db"
    conn = None
    cursor = None

    def ensure_existing(self, database_path="./resources/database.db"):
        self.database_path = database_path
        conn = sqlite3.connect(self.database_path)
        conn.cursor().execute('''CREATE TABLE IF NOT EXISTS maintable
                     (key TEXT PRIMARY KEY, value TEXT)''')
        conn.close()

    def __init__(self):
        self.ensure_existing()
        self.conn = sqlite3.connect(self.database_path)
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    def insert_new_pair(self, key: str, value: str) -> None:
        self.cursor.execute("INSERT INTO maintable VALUES (?, ?)", (key, value))
        self.conn.commit()

    def get_value(self, key: str) -> Optional[list[Any]]:
        """
        Returns the value of a key
        :param key:
        :return value:
        """
        self.cursor.execute("SELECT key, value FROM maintable WHERE key LIKE ?", (f"%{key}%",))
        try:
            return self.cursor.fetchall()
        except Exception as e:
            with open("dbLogs.txt", "w") as fil:
                fil.write(str(e))
            return "[ Not Found ]"

    def delete_pair(self, key: str) -> bool:
        try:
            self.cursor.execute("DELETE FROM maintable WHERE key = ?", (key,))
            self.conn.commit()
            return True
        except sqlite3.OperationalError:
            return False

    def update_value(self, key: str, value: str) -> None:
        try:
            self.cursor.execute("UPDATE maintable SET value = ? WHERE key = ?", (value, key))
            self.conn.commit()
        except Exception as e:
            print(e)

    def get_all_keys(self):
        self.cursor.execute("SELECT key FROM maintable")
        return [row[0] for row in self.cursor.fetchall()]

    def get_key_by_value(self, value: str) -> Union[list[Any], str]:
        "Get the key of respective pair using the value as a key"
        self.cursor.execute("SELECT key, value FROM maintable WHERE value LIKE ?", (f"%{value}%",))
        try:
            return self.cursor.fetchall()
        except Exception as e:
            with open("dbLogs.txt", "w") as fil:
                fil.write(str(e))
            return "[ Not Found ]"
