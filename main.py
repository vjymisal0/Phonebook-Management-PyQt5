from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import mysql.connector
import sys
from MainWindow import MainWindow
from dbconnect import mydb

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
