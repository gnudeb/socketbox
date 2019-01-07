import sqlite3
from threading import Lock


class NoSuchKeyError(Exception):
    pass


class Storage:

    def store(self, key, value):
        raise NotImplementedError

    def retrieve(self, key):
        raise NotImplementedError


class DictStorage(Storage):

    def __init__(self):
        self.dict = {}

    def store(self, key, value):
        self.dict[key] = value

    def retrieve(self, key):
        try:
            return self.dict[key]
        except KeyError:
            raise NoSuchKeyError(key)


class SQLiteStorage(Storage):

    def __init__(self, database="storage.db"):
        self.connection = sqlite3.connect(database, check_same_thread=False)
        self._lock = Lock()

        self._setup()

    def store(self, key, value):
        with self._lock:
            self.connection.execute(
                "INSERT INTO Storage VALUES (?, ?)",
                (key, value)
            )
            self.connection.commit()

    def retrieve(self, key):
        with self._lock:
            cursor = self.connection.execute(
                "SELECT value FROM Storage WHERE key = ?",
                (key,)
            )
            row = cursor.fetchone()

        if row is None:
            raise NoSuchKeyError(key)

        value = row[0]
        return value

    def _setup(self):
        self.connection.execute(
            "CREATE TABLE IF NOT EXISTS Storage ("
            "   key VARCHAR(64) PRIMARY KEY,"
            "   value VARCHAR(64)"
            ");"
        )
        self.connection.commit()
