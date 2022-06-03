import sqlite3
import secrets
import enum
from PyQt6.QtCore import Qt, QDate
from sqlite3 import Error

errorMsgsOn = False

class tableType(enum.Enum):
    """Determines the type of table (what behavior the habits follow)"""
    onePercent = 1

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

def createContentColumnTable(connection, tableType, tableName = generateName()):
    """Create a table in the connected database for a new column."""
    createCmd = f"""
        CREATE TABLE {tableName} (
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
        if errorMsgsOn:
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
        SELECT date, value, cumulative FROM {tableName} WHERE date = '{date}'
    """

    cursor = connection.cursor()
    cursor.execute(fetchCmd)

    return cursor.fetchone()

sampleNumDays = 30

def main():
    currentDate = QDate.currentDate()
    days = [currentDate]
    dayStrings = [currentDate.toString(Qt.DateFormat.ISODate)]
    for i in range(sampleNumDays):
        days.append(days[-1].addDays(-1))
        dayStrings.append(days[-1].toString(Qt.DateFormat.ISODate))

    lastDate = days[-1]
    print(currentDate.daysTo(lastDate))

    dbName = "testing.db"
    tblName = "normalTbl"
    myConnection = createConnection(dbName)
    if myConnection is not None:
        print(f"Successfully connected to {dbName}")
        createContentColumnTable(myConnection, tblName)
        print(fetchEntry(myConnection, tblName, "2022-05-06"))


    myConnection.close()

if __name__ == '__main__':
    main()