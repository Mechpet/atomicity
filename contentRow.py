from xmlrpc.client import Boolean
from PyQt6.QtWidgets import QHBoxLayout, QWidget
from PyQt6.QtCore import QSettings, QEvent, Qt, QMimeData, pyqtSignal
from PyQt6.QtGui import QDrag, QPixmap, QPainter, QCursor
from math import floor
import os

from contentHead import contentHead

# Layout of contentHeaders in a horizontal row
class contentRow(QWidget):
    """A row of contentHeads."""
    horScroll = pyqtSignal(Boolean)
    showColumn = pyqtSignal(int)
    def __init__(self):
        super().__init__()

        # Install continuous mouse tracking
        self.dragged = None
        self.setAcceptDrops(True)
        self.setMouseTracking(True)
        #self.installEventFilter(self)

        self.settings = QSettings("Mechpet", "Atomicity")
        self.settings.beginGroup("contentRow")

        self.selected = None
        self.change = False

        self.layout = QHBoxLayout()

        if self.settings.value("num"):
            for i in range(int(self.settings.value("num"))):
                self.layout.addWidget(contentHead(i, self))
        else:
            # The key "num" is not a QString of an integer
            self.settings.setValue("num", 0)

        self.setLayout(self.layout)

    def dragEnterEvent(self, event):
        """Display the cursor as accepting drag-and-drop events"""
        self.change = False
        event.accept()

    def dragMoveEvent(self, event):
        """As the dragged widget moves, show the preview of the contentRow"""
        hovering = self.getSelectedBinary(event.position().x(), event.position().y())
        if hovering is not None and self.selected is not None and hovering is not self.selected:
            # Re-arrange the layout:
            self.rearrange(self.layout.indexOf(hovering))
            self.change = True
    
    def dropEvent(self, event):
        """After the drag completes, save the settings"""
        # If there may have been a change to the layout, rewrite the settings
        print("Leave event!")
        if self.change:
            print("Change detected!")
            # Rename the dragged widget's settings to a temporary file
            os.rename(f"contentHead{self.selected.index}.ini", "temp.ini")
            # Rename all the involved files
            self.renameHeads(self.selected.index, self.layout.indexOf(self.selected))
            # Finalize the dragged widget's setting file name
            os.rename("temp.ini", f"contentHead{self.layout.indexOf(self.selected)}.ini")

    def rearrange(self, index):
        """Remove the selected widget and re-insert it back to a specified index"""
        self.layout.removeWidget(self.selected)
        self.layout.insertWidget(index, self.selected)
        
    def addHeader(self):
        """Append a new contentHead to the list"""
        # Create a new contentHead devoid of settings
        self.layout.addWidget(contentHead(self.layout.count(), self))
        self.settings.setValue("num", self.layout.count())

        self.setLayout(self.layout)

        self.layout.itemAt(self.layout.count() - 1).widget().settingsWindow()

    def eventFilter(self, object, event):
        """Filter mouse events"""
        result = False
        if object is self:
            if event.type() == QEvent.Type.MouseButtonPress:
                self.mousePressEvent(event)
            elif event.type() == QEvent.Type.MouseMove:
                self.mouseMoveEvent(event)
            elif event.type() == QEvent.Type.MouseButtonRelease:
                self.mouseReleaseEvent(event)
        return result

    def mousePressEvent(self, event):
        """When the mouse left-clicks on a contentHead, store information about the item being moved"""
        print("Mouse pressed")
        if event.button() == Qt.MouseButton.LeftButton:
            self.selected = self.getSelectedBinary(event.position().x(), event.position().y())
        elif event.button() == Qt.MouseButton.MiddleButton:
            self.horScroll.emit(True)
            self.setCursor(QCursor(QCursor(Qt.CursorShape.SizeHorCursor)))
    
    def mouseMoveEvent(self, event):
        """When the mouse moves and has selected a widget, enable dragging and dropping of the widget"""
        # If the user just selected a widget: (must initialize the drag instance)
        if event.buttons() & Qt.MouseButton.LeftButton and self.selected is not None:
            # Grab a pixmap of the full widget
            pixmapOpaque = self.selected.grab()

            # Create an empty transparent pixmap to paint on
            pixmap = QPixmap(self.selected.geometry().width(), self.selected.geometry().height())
            pixmap.fill(Qt.GlobalColor.transparent)

            # Paint in a transparent version of the widget to be dragged
            painter = QPainter(pixmap)
            painter.setOpacity(0.33)
            painter.drawPixmap(0, 0, pixmapOpaque)
            painter.end()

            mimedata = QMimeData()
            mimedata.setImageData(pixmap)

            self.dragged = QDrag(self.selected)
            self.dragged.setMimeData(mimedata)
            self.dragged.setPixmap(pixmap)

            # Set the drag image at the cursor location
            self.dragged.setHotSpot(event.pos() - self.selected.pos())
            self.dragged.exec()

            # Clear the instances after execution is over
            self.dragged = None
            self.selected = None

    def getSelectedBinary(self, x, y):
        """Get the item index of the content using binary search"""
        low = 0
        high = self.layout.count() - 1

        while low <= high:
            mid = floor((high + low) / 2)
        
            if self.layout.itemAt(mid).geometry().contains(x, y):
                return self.layout.itemAt(mid).widget()
            elif self.layout.itemAt(mid).geometry().x() < x:
                low = mid + 1
            elif self.layout.itemAt(mid).geometry().x() > x:
                high = mid - 1
        return None

    def deleteHead(self, index):
        """Deletes a contentHead from the row; assumes that the contentHead exists"""
        # Delete all references to the widget
        self.layout.itemAt(index).widget().close()
        self.layout.removeWidget(self.layout.itemAt(index).widget())
        self.settings.setValue("num", self.layout.count())

    def renameHeads(self, start, end):
        """Rename all the contentHead ini files starting from the given index assuming the given setting file is neglible"""
        filePrefix = "contentHead"
        if end < 0:
            # Signals to rename to the end
            end = self.layout.count()
        if start >= end:
            step = -1
        else:
            step = 1
        # Shift the start position by 1 widget (rightward if moving right, leftward if moving left) 
        for i in range(start + step, end + step, step):
            os.rename(f"{filePrefix}{str(i)}.ini", f"{filePrefix}{str(i - step)}.ini")
            self.layout.itemAt(i).widget().index = i - step
