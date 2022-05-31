from PyQt6.QtWidgets import QHBoxLayout, QWidget, QStackedLayout
from PyQt6.QtCore import QSettings, QEvent, Qt, QMimeData
from PyQt6.QtGui import QDrag, QPixmap
from math import floor
import os

from contentHead import contentHead

# Layout of contentHeaders in a horizontal row
class contentRow(QWidget):
    """A row of contentHeads."""
    def __init__(self):
        super().__init__()

        # Install continuous mouse tracking
        self.dragged = None
        self.setAcceptDrops(True)
        self.setMouseTracking(True)
        self.installEventFilter(self)

        self.settings = QSettings("Mechpet", "Atomicity")
        self.settings.beginGroup("contentRow")

        self.list = []
        self.selected = None

        self.layout = QHBoxLayout()

        if self.settings.value("num"):
            for i in range(int(self.settings.value("num"))):
                self.list.append(contentHead(i, self))
                self.layout.addWidget(self.list[-1])
        else:
            # The key "num" is not a QString of an integer
            self.settings.setValue("num", 0)

        self.setLayout(self.layout)

    def dragEnterEvent(self, e):
        """Display the cursor as accepting drag-and-drop events"""
        e.accept()

    def dragMoveEvent(self, e):
        """As the dragged widget moves, show the preview of the contentRow"""
        print(f"Event position = ({e.position().x()}, {e.position().y()})")
        
    def addHeader(self):
        """Append a new contentHead to the list"""
        # Create a new contentHead devoid of settings
        self.list.append(contentHead(len(self.list), self))
        # Set the index of the contentHead to be at the end of the row
        self.layout.addWidget(self.list[-1])
        self.settings.setValue("num", len(self.list))

        self.setLayout(self.layout)

        self.list[-1].settingsWindow()

    def eventFilter(self, object, event):
        """Filter mouse events"""
        res = False
        if object is self:
            if event.type() == QEvent.Type.MouseButtonPress:
                self.mousePressEvent(event)
            elif event.type() == QEvent.Type.MouseMove:
                self.mouseMoveEvent(event)
        return res

    def mousePressEvent(self, event):
        """When the mouse left-clicks on a contentHead, store information about the item being moved"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.getSelectedBinary(event.position().x(), event.position().y())
    
    def mouseMoveEvent(self, event):
        """When the mouse moves and has selected a widget, enable dragging and dropping of the widget"""
        # If the user just selected a widget: (must initialize the drag instance)
        if event.buttons() & Qt.MouseButton.LeftButton and self.selected is not None:
            # Set the dragged image to the selected widget
            pixmap = QPixmap(self.selected.size().width(), self.selected.size().height())
            pixmap.fill(Qt.GlobalColor.white)
            pixmapOld = self.selected.grab()
            mimedata = QMimeData()
            mimedata.setImageData(pixmap)

            self.dragged = QDrag(self.selected)
            self.dragged.setMimeData(mimedata)
            self.dragged.setPixmap(pixmap)

            # Set the drag image at the cursor location
            self.dragged.setHotSpot(event.pos() - self.selected.pos())
            self.dragged.exec()

            # Clear the instances
            self.dragged = None
            self.selected = None

    def getSelectedLinear(self, x, y):
        """Get the item index of the content using linear search"""
        for widget in self.list:
            # Iterate through list of contentHeads, looking for the one that the user selected
            if widget.geometry().contains(x, y):
                # Found the contentHead that the user clicked on; end method
                self.selected = widget
                return

    def getSelectedBinary(self, x, y):
        """Get the item index of the content using binary search"""
        low = 0
        high = len(self.list) - 1

        while low <= high:
            mid = floor((high + low) / 2)
        
            if self.list[mid].geometry().contains(x, y):
                self.selected = self.list[mid]
                return 
            elif self.list[mid].geometry().x() < x:
                low = mid + 1
            elif self.list[mid].geometry().x() > x:
                high = mid - 1
        return 

    def deleteHead(self, index):
        """Deletes a contentHead from the row; assumes that the contentHead exists"""
        # Delete all references to the widget
        self.layout.removeWidget(self.list[index])
        del self.list[index]
        self.settings.setValue("num", len(self.list))

    def renameHeads(self, index):
        """Rename all the contentHead ini files starting from the given index"""
        filePrefix = "contentHead"
        os.remove(f"{filePrefix}{str(index)}.ini")
        for i in range(index + 1, len(self.list) + 1):
            os.rename(f"{filePrefix}{str(i)}.ini", f"{filePrefix}{str(i - 1)}.ini")

    def showAllGeometries(self):
        for item in self.list:
            print(f"Geometry = {item.geometry()}")