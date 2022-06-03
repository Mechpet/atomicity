import sqlite3
import secrets
from sqlite3 import Error
from venv import create

def generateName():
    """Generate a pseudo-random name that has no defining properties"""
    name = secrets.token_hex(64)
    return name

def createConnection(dbFile):
    """Create a connection to the database."""
    connection = None
    # Try to connect to the passed .db file
    try:
        connection = sqlite3.connect(dbFile)
    except Error as e:
        print(f"EXCEPTION: {e} while creating connection")
    return connection

def createContentColumnTable(connection, tableName = generateName()):
    """Create a table in the connected database for a new column."""
    createCmd = f"""
        CREATE TABLE IF NOT EXISTS {tableName} (
        date text PRIMARY KEY NOT NULL,
        value integer,
        cumulative real
    );
    """
    try:
        cursor = connection.cursor()
        cursor.execute(createCmd)
        return True
    except Error as e:
        print(f"EXCEPTION: {e} while creating table")
        return False

def upsertDay(connection, tableName, date, value, cumulative):
    """Write to the database to the appropriate table with the given values"""
    insertCmd = f"""
        INSERT INTO {tableName} 
        (date, value, cumulative)
        VALUES(?, ?, ?)
        ON CONFLICT(date)
        DO UPDATE SET value = excluded.value, cumulative = excluded.cumulative
    """
    insertValues = (date, value, cumulative)

    cursor = connection.cursor()
    cursor.execute(insertCmd, insertValues)
    connection.commit()

def main():
    dbName = "testing.db"
    tblName = "normalTbl"
    myConnection = createConnection(dbName)
    if myConnection is not None:
        print(f"Successfully connected to {dbName}")
        createContentColumnTable(myConnection, tblName)
        upsertDay(myConnection, tblName, "1-January-2024", 0, 1)
        upsertDay(myConnection, tblName, "5-August-2021", 1, 0)
        upsertDay(myConnection, tblName, "2-June-2022", 2, 5)
        upsertDay(myConnection, tblName, "10-February-2020", 0, 1)

    myConnection.close()

if __name__ == '__main__':
    main()