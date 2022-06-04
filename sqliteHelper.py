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
    name = secrets.token_hex(16)
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
        CREATE TABLE {tableName} (
        date text PRIMARY KEY NOT NULL,
        value integer,
        cumulative real
    );
    """
    try:
        cursor = connection.cursor()
        cursor.execute(createCmd)
        indexCmd = f"""
            CREATE UNIQUE INDEX indexDate
            ON {tableName} (date);
        """
        #cursor.execute(indexCmd)
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

def fetchConsecutive(connection, tableName, date, entries):
    return

def initTable(connection, tableName, startDate):
    """Initialize a table with empty entries"""
    days = [startDate]
    for i in range(startDate.daysTo(QDate.currentDate())):
        days.append(days[i].addDays(1))
    
    for day in days:
        upsertDay(connection, tableName, day.toString(Qt.DateFormat.ISODate), None, 1.00)
    
connection = createConnection(r"database\info.db")
