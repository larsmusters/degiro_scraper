import pandas as pd
import sqlite3


class DatabaseHandler():
    DB_FILE = 'database/database.db'
    SCHEMA_FILE = 'database/schema.sql'


    def __init__(self):
        self.conn = sqlite3.connect(DatabaseHandler.DB_FILE)
        self.cursor = self.conn.cursor()
        self.create_table()


    def create_table(self):
        with open(DatabaseHandler.SCHEMA_FILE, 'r') as rf:
            schema = rf.read()
        self.conn.executescript(schema)


    def insert_data(self):
        with open('database/example.sql', 'r') as rf:
            basic_insert = rf.read()
        self.conn.executescript(basic_insert)
    

    def get_all_data(self):
        return pd.read_sql("SELECT * FROM data", self.conn)
    

    def empty_db(self):
        self.cursor.execute("DELETE FROM data")
        self.conn.commit()


    def __exit__(self, ext_type, exc_value, traceback):
        self.cursor.close()
        if isinstance(exc_value, Exception):
            self.connection.rollback()
        else:
            self.connection.commit()
        self.connection.close()



if __name__ == "__main__":
    handler = DatabaseHandler()
    handler.create_table()