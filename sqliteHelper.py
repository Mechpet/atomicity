import sqlite3
import random
import secrets
from PyQt6.QtCore import Qt, QDate
from sqlite3 import Error

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

def dropTable(connection, tableName):
    """Delete an entire table"""
    deleteCmd = f"""
        DROP TABLE {tableName}
    """
    
    cursor = connection.cursor()
    cursor.execute(deleteCmd)
    connection.commit()

def fetchEntry(connection, tableName, date):
    """Fetch a single entry with the given date"""
    fetchCmd = f"""
        SELECT date, value, cumulative FROM {tableName} WHERE date = '{date}';
    """

    return


sampleNumDays = 30

def main():
    currentDate = QDate.currentDate()
    days = [currentDate]
    dayStrings = [currentDate.toString(Qt.DateFormat.ISODate)]
    for i in range(sampleNumDays):
        days.append(days[-1].addDays(-1))
        dayStrings.append(days[-1].toString(Qt.DateFormat.ISODate))

    dbName = "testing.db"
    tblName = "normalTbl"
    myConnection = createConnection(dbName)
    if myConnection is not None:
        print(f"Successfully connected to {dbName}")
        createContentColumnTable(myConnection, tblName)
        for i in range(sampleNumDays):
            upsertDay(myConnection, tblName, dayStrings[i], random.randint(0, 1), random.randint(0, 100))

        upsertDay(myConnection, tblName, dayStrings[1], 2, random.randint(0, 100))        

    myConnection.close()

if __name__ == '__main__':
    main()