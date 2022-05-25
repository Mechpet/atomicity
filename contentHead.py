# Header of each column (topmost block of data that is static to vertical scrolling)
from PyQt6.QtWidgets import QWidget, QPushButton, QDialog, QGridLayout, QLabel
from PyQt6.QtGui import QPainter, QPainterPath, QBrush, QPen, QColor, QTextOption, QCursor, QIcon
from PyQt6.QtCore import Qt, QRectF, QSize, QSettings, QFile
from settingsWindow import contentHeadSettingsWindow

# # # Attributes:
# `size` = Width and height of the contentHead widget (box-shaped, user-customizable) {int}.
# `text` = Main description of the contentHead widget (to be displayed in the center; adjustable via `settingsWindow`) {str}.
# `color` = Color of the contentHead widget's body (adjustable via `settingsWindow`) {QColor}.
# `index` = Position in the contentRow (negative implies that the contentHead is newly constructed) {int}.
class contentHead(QWidget):
    """A block that acts as the head of the list of contentCells."""
    def __init__(self, index):
        super().__init__()

        self.index = index

        self.initUI()

    def initUI(self):
        self.minSize = 100
        self.maxSize = 200
        self.setMinimumSize(self.minSize, self.minSize)
        self.setMaximumSize(self.maxSize, self.maxSize)
        if self.index >= 0:
            # Open the correct settings file
            self.initSettings()
            self.fetch()
        else:
            # Default settings
            self.index = abs(self.index + 1)
            # Open the correct settings file
            self.initSettings()
            self.default()

        self.layout = QGridLayout()
        # Customize the 'Settings' button
        self.btn = QPushButton("", self)
        self.btn.resize(QSize(25, 25))
        #self.btn.move(self.size * 0.05, self.size * 0.85)
        self.btn.setToolTip("<b>Settings</b>")
        self.btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn.setProperty("opened", False)
        self.btn.setStyleSheet("""
            QPushButton {
                border: 0px;
                background: transparent;
                border-image: url(images/appIcons/cogwheel_idle.png);
            }
            QPushButton:hover {
                border-image: url(images/appIcons/cogwheel_hover.png);
            }
        """)
        self.btn.clicked.connect(self.settingsWindow)
        self.iconBtn = QPushButton("Icon", self)
        self.iconBtn.setStyleSheet("""
            QPushButton {
                border: 0px;
                background: transparent;
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
        
        self.layout.addWidget(self.btn, 0, 0)
        self.layout.addWidget(self.iconBtn, 0, 1)
        self.setLayout(self.layout)

        print("SUP")


    def paintEvent(self, e):
        qp = QPainter(self)
        #qp.begin(self)

        col = QColor(0, 0, 0)
        col.setNamedColor('#d4d4d4')

        qp.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        path = QPainterPath()

        pen = QPen(col, 0.5)
        qp.setPen(pen)
        brush = QBrush(self.color)
        qp.setBrush(brush)

        #rect = QRectF(e.rect())
        rect = QRectF(0, 0, 200, 200)
        rect.adjust(0.0, 0.0, 1, 1)
        path.addRoundedRect(rect, 10, 10)
        qp.setClipPath(path)
        qp.fillPath(path, qp.brush())
        qp.strokePath(path, qp.pen())
        qp.drawText(rect, self.text, QTextOption(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop))

        qp.end()

    def settingsWindow(self):
        # Doesn't work yet: when opened, change appearance of the pushButton
        self.btn.setProperty("opened", True)
        self.window = contentHeadSettingsWindow(0, 0, 500, 500, self.text, self.color)
        self.window.apply.connect(self.updateData)
        self.window.show()

    def setIcon(self):
        self.settingsWindow()
        self.window.openFileDialog()
        if QFile.exists(self.iconPath):
            self.alert.close()

    def initSettings(self):
        self.settingName = f"contentHead{self.index}.ini"
        self.settings = QSettings(self.settingName, QSettings.Format.IniFormat)

    def updateData(self, newName, color, newIconPath):
        """[Slot] Update the contentHead's text"""
        self.text = newName
        self.color = color
        if self.window.verifyFile(newIconPath):
            self.iconPath = newIconPath
            newIcon = QIcon(self.iconPath)
            self.iconBtn.setIcon(newIcon)
        self.synchronize()
    
    def synchronize(self):
        """Update all of the settings of the contentHead"""
        self.settings.setValue("text", self.text)
        self.settings.setValue("red", self.color.red())
        self.settings.setValue("green", self.color.green())
        self.settings.setValue("blue", self.color.blue())
        self.settings.setValue("path", self.iconPath)
        self.settings.sync()

    def fetch(self):
        """Sets all of its attributes based on the settings"""
        self.text = self.settings.value("text")
        self.color = QColor(int(self.settings.value("red")), int(self.settings.value("green")), int(self.settings.value("blue")))
        self.iconPath = self.settings.value("path")

    def default(self):
        """Sets all of its attributes to default settings and saves settings"""
        self.text = None
        self.color = QColor(55, 55, 55)
        self.iconPath = None

        self.synchronize()