# The main window of the application 
import sys

from PyQt6.QtWidgets import QApplication, QWidget, QTextEdit, QPushButton
from contentCell import contentCell

def main():
    app = QApplication(sys.argv)

    window = QWidget()
    window.setWindowTitle("Atomicity")
    
    c.move(200, 200)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()