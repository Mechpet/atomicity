import sqlite3
from sqlite3 import Error

def createConnection(dbFile):
    """Create a connection to the database."""
    conn = None
    # Try to connect to the passed .db file
    try:
        conn = sqlite3.connect(dbFile)
        return conn
    except Error as e:
        print(f"EXCEPTION: {e} while creating connection")
    return conn

def createTable(conn, createTableSql):
    """Create a table in the connected database."""
    try:
        cursor = conn.cursor()
        cursor.execute(createTableSql)
    except Error as e:
        print(f"EXCEPTION: {e} while creating table")

def createContentColumn(conn, contentSettings):
    """Create a table for a new column"""
    sqlCmd = """INSERT INTO contentHeaders(date, value, cumulative)
             VALUES(?, ?, ?)"""
    cursor = conn.cursor()
    cursor.execute(sqlCmd, contentSettings)
    conn.commit()
    return cursor.lastrowid

def updateContentColumn(conn, tableName, task):
    return
