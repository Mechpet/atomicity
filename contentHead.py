# Header of each column (topmost block of data that is static to vertical scrolling)
from multiprocessing import connection
from PyQt6.QtWidgets import QWidget, QPushButton, QDialog, QGridLayout, QLabel
from PyQt6.QtGui import QPainter, QPainterPath, QBrush, QPen, QColor, QTextOption, QCursor, QIcon
from PyQt6.QtCore import Qt, QRectF, QSettings, QSize, QFile, QDate
import os
from stat import S_IREAD, S_IRGRP, S_IROTH, S_IWUSR

from settingsWindow import contentHeadSettingsWindow
import sqliteHelper as sql

contentHeadRect = QRectF(0, 0, 200, 200)
contentHeadRect.adjust(0.0, 0.0, 1, 1)

# # # Attributes:
# `size` = Width and height of the contentHead widget (box-shaped, user-customizable) {int}.
# `text` = Main description of the contentHead widget (to be displayed in the center; adjustable via `settingsWindow`) {str}.
# `color` = Color of the contentHead widget's body (adjustable via `settingsWindow`) {QColor}.
# `index` = Position in the contentRow (negative implies that the contentHead is newly constructed) {int}.
class contentHead(QWidget):
    """A block that acts as the head of the list of contentCells."""
    def __init__(self, index, parent = None):
        super().__init__(parent)
        self.setMouseTracking(True)
        self.setCursor(QCursor(Qt.CursorShape.OpenHandCursor))

        self.index = index
        self.parent = parent

        self.initUI()

    def initUI(self):
        self.size = 200
        self.setFixedSize(self.size, self.size)
        if self.initSettings():
            # Settings exist already; just fetch the data
            self.fetch()
        else:
            # Settings don't exist already; default the data
            self.default()

        self.layout = QGridLayout()
        # Customize the 'Settings' button
        self.btn = QPushButton("", self)
        self.btn.resize(QSize(75, 75))
        #self.btn.move(self.size * 0.05, self.size * 0.85)
        self.btn.setToolTip("<b>Settings</b>")
        self.btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn.setProperty("opened", False)
        self.btn.setStyleSheet("""
            QPushButton {
                border: 0px;
                background: transparent;
                width: 20px;
                height: 20px;
                border-image: url(images/appIcons/cogwheel_idle.png);
            }
            QPushButton:hover {
                border-image: url(images/appIcons/cogwheel_hover.png);
            }
        """)
        self.btn.clicked.connect(self.settingsWindow)
        self.iconBtn = QPushButton("", self)
        self.iconBtn.resize(QSize(75, 75))
        self.iconBtn.setStyleSheet("""
            QPushButton {
                border: 0px;
                background: transparent;
                qproperty-iconSize: 50px;
            }
        """)
        if self.iconPath:
            if QFile.exists(self.iconPath):
                # Path given to icon image exists: able to construct a visible icon
                newIcon = QIcon(self.iconPath)
                self.iconBtn.setIcon(newIcon)
            else:
                # Path given to icon image doesn't exist: alert user
                self.alert = QDialog()
                layout = QGridLayout()
                layout.addWidget(QLabel(f"Icon path {self.iconPath} was not found."), 0, 0)
                fixBtn = QPushButton("Set new icon")
                fixBtn.clicked.connect(self.setIcon)
                layout.addWidget(fixBtn, 0, 1)
                self.alert.setLayout(layout)
                self.alert.exec()
        
        
        for i in range(10):
            self.layout.setColumnStretch(i, 1)
        self.layout.addWidget(self.iconBtn, 0, 0, 3, 3)
        self.layout.addWidget(self.btn, 0, 9, 1, 1)
        self.setLayout(self.layout)
        
    def paintEvent(self, e):
        """Paint the rounded rectangular shape of the contentHead based on the selected color"""
        qp = QPainter(self)

        # Initialize a pen color
        col = QColor(0, 255, 0)
        # Set pen color to outline color
        col.setNamedColor('#d4d4d4')

        qp.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        path = QPainterPath()

        outlinePen = QPen(col, 1.5)
        qp.setPen(outlinePen)
        brush = QBrush(self.cellColor)
        qp.setBrush(brush)

        path.addRoundedRect(contentHeadRect, 10, 10)
        qp.setClipPath(path)
        qp.fillPath(path, qp.brush())
        qp.strokePath(path, qp.pen())

        # Set the text color
        textPen = QPen(self.textColor, 0.5)
        qp.setPen(textPen)
        qp.drawText(contentHeadRect, self.text, QTextOption(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop))

        qp.end()

    def settingsWindow(self):
        """Open a new window that takes priority over the main application"""
        self.btn.setProperty("opened", True)
        self.window = contentHeadSettingsWindow(0, 0, 500, 500, self.text, self.cellColor, self.textColor, self.iconPath, self)
        self.window.apply.connect(self.updateData)
        self.window.show()

    def setIcon(self):
        """Set the icon of the contentHead quickly"""
        self.settingsWindow()
        self.window.openFileDialog()
        if QFile.exists(self.iconPath):
            self.alert.close()

    def initSettings(self):
        """Initialize the settings attribute to what it *should* be"""
        self.settingName = f"contentHead{self.index}.ini"
        self.settings = QSettings(self.settingName, QSettings.Format.IniFormat)
        return QFile.exists(self.settingName)

    def updateData(self, newName, newCellColor, newTextColor, newIconPath):
        """[Slot] Update the contentHead's text"""
        self.text = newName
        self.cellColor = newCellColor
        self.textColor = newTextColor
        # If the passed path exists, able to set the icon
        if self.window.verifyFile(newIconPath):
            self.iconPath = newIconPath
            newIcon = QIcon(self.iconPath)
            self.iconBtn.setIcon(newIcon)
        else:
            # Set current icon to null
            self.iconPath = None
            self.iconBtn.setIcon(QIcon())
        # Update on local device
        self.synchronize()
    
    def synchronize(self):
        """Update all of the settings of the contentHead"""
        # Make the file writeable and readable
        try:
            os.chmod(self.settingName, S_IWUSR | S_IREAD)
        except FileNotFoundError:
            pass
        self.settings.setValue("text", self.text)
        self.settings.setValue("cellRed", self.cellColor.red())
        self.settings.setValue("cellGreen", self.cellColor.green())
        self.settings.setValue("cellBlue", self.cellColor.blue())
        self.settings.setValue("textRed", self.textColor.red())
        self.settings.setValue("textGreen", self.textColor.green())
        self.settings.setValue("textBlue", self.textColor.blue())
        self.settings.setValue("path", self.iconPath)
        self.settings.sync()
        # Make the file read-only
        try:
            os.chmod(self.settingName, S_IREAD | S_IRGRP | S_IROTH)
        except FileNotFoundError:
            print(f"EXCEPTION: File {self.settingName}'s operation failed.")

    def fetch(self):
        """Sets all of its attributes based on the currently set settings"""
        self.text = self.settings.value("text")
        self.cellColor = QColor(int(self.settings.value("cellRed")), int(self.settings.value("cellGreen")), int(self.settings.value("cellBlue")))
        self.textColor = QColor(int(self.settings.value("textRed")), int(self.settings.value("textGreen")), int(self.settings.value("textBlue")))
        self.iconPath = self.settings.value("path")

    def default(self):
        """Sets all of its attributes to default settings and saves settings"""
        self.text = None
        self.cellColor = QColor(55, 55, 55)
        self.textColor = QColor(0, 0, 0)
        self.iconPath = None

        # Create a new unique table
        tableName = sql.generateName()
        while sql.createContentColumnTable(sql.connection, tableName) is False:
            tableName = sql.generateName()

        self.settings.setValue("table", tableName)
        sql.initTable(sql.connection, tableName, QDate(2022, 5, 16))

        self.synchronize()
    
    def delData(self):
        """Delete the instance"""
        if self.parent is not None:
            sql.dropTable(sql.connection, self.settings.value("table"))
            self.parent.deleteHead(self.index)
            os.chmod(f"contentHead{str(self.index)}.ini", S_IWUSR | S_IREAD)
            os.remove(f"contentHead{str(self.index)}.ini")
            self.parent.renameHeads(self.index, -1)
            self.window.instance = None
            self.window.dialog.close()
            self.window.close()
        else:
            print("Parent is None")
