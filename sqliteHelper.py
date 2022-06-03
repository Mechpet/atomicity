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

def insertDay(connection, tableName, date, value):
    """Write to the database to the appropriate table with the given values"""
    insertCmd = f"""
        INSERT INTO {tableName} 
        (date, value, cumulative)
        VALUES(?, ?, ?)"""
    insertValues = (date, value, 0)

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
        #insertDay(myConnection, tblName, "2-June-2022", 1)

    myConnection.close()

if __name__ == '__main__':
    main()