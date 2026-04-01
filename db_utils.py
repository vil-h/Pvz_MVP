import sqlite3
def get_connection():
    con = sqlite3.connect("database.db")
    return con


def close_connection(con):
    con.close()
