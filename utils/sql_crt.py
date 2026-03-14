import sqlite3

class SQLCtr:
    def __init__(self, path):
        self.conn = sqlite3.connect(path)
        self.conn.row_factory = sqlite3.Row
        self.cur = self.conn.cursor()

    def execute(self, command, params=None):
        if params:
            self.cur.execute(command, params)
        else:
            self.cur.execute(command)

        self.conn.commit()
        return self.cur.fetchall()

    def create_table(self, table_name, column):
        self.cur.execute(
            f"CREATE TABLE IF NOT EXISTS {table_name} ({column})"
        )
        self.conn.commit()
    
    def insert(self, table_name: str, data: dict):
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?"] * len(data))
        values = tuple(data.values())

        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        self.cur.execute(sql, values)
        self.conn.commit()
    
    def select(self, table_name:str) -> list:
        self.cur.execute(f"SELECT * FROM {table_name}")
        
        return [dict(row) for row in self.cur.fetchall()]
    
    def close(self):
        self.cur.close()
        self.conn.close()