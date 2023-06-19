import pandas as pd
import sqlite3


class DatabaseHandler():
    DB_FILE = 'database/database.db'
    SCHEMA_FILE = 'database/config/schema.sql'


    def __init__(self):
        self.conn = sqlite3.connect(DatabaseHandler.DB_FILE)
        self.cursor = self.conn.cursor()
        self.create_table()


    def create_table(self):
        with open(DatabaseHandler.SCHEMA_FILE, 'r') as rf:
            schema = rf.read()
        self.conn.executescript(schema)


    def insert_data(self, df):
        df.to_sql('data', self.conn, if_exists='append', index=False)
        self.conn.commit()
    

    def get_all_data(self):
        return pd.read_sql("SELECT * FROM data", self.conn)
    

    def get_data_by_name(self, name):
        return pd.read_sql(f"SELECT * from data where product='{name}'", self.conn)

    def empty_db(self):
        self.cursor.execute("DELETE FROM data")
        self.conn.commit()


    def __exit__(self, ext_type=None, exc_value=None, traceback=None):
        self.cursor.close()
        if isinstance(exc_value, Exception):
            self.conn.rollback()
        else:
            self.conn.commit()
        self.conn.close()



if __name__ == "__main__":
    handler = DatabaseHandler()
    handler.create_table()