from config import SQL_PATHs
from utils.sql_crt import SQLCtr

def init():
    SQL = SQLCtr(SQL_PATHs["wiki"])
    SQL.create_table("Pages", """
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    thread_id INTEGER
                    """)