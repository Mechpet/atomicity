from PyQt6.QtGui import QColor
from PyQt6.QtCore import QSettings

cellColor = QColor(55, 55, 55)
textColor = QColor(0, 0, 0)
numDays = 14
minNumDays = 1

def fetchColors():
    settings = QSettings("Mechpet", "Atomicity")
    settings.beginGroup("global")

    fetchedCellColor = settings.value("cellColor")
    fetchedTextColor = settings.value("textColor")

    return fetchedCellColor, fetchedTextColor

def fetchDays():
    settings = QSettings("Mechpet", "Atomicity")
    settings.beginGroup("global")

    numDays = settings.value("numDays")

    return numDays