from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import mysql.connector
from dbconnect import mydb


class EditContactDialog(QDialog):
    def __init__(self, name, phone, email, parent=None):
        super().__init__(parent)
        self.name_label = QLabel("Name:")
        self.name_line_edit = QLineEdit(name)
        self.phone_label = QLabel("Phone:")
        self.phone_line_edit = QLineEdit(phone)
        self.email_label = QLabel("Email:")
        self.email_line_edit = QLineEdit(email)
        self.save_button = QPushButton("Save")
        self.cancel_button = QPushButton("Cancel")

        layout = QGridLayout()
        layout.addWidget(self.name_label, 0, 0)
        layout.addWidget(self.name_line_edit, 0, 1)
        layout.addWidget(self.phone_label, 1, 0)
        layout.addWidget(self.phone_line_edit, 1, 1)
        layout.addWidget(self.email_label, 2, 0)
        layout.addWidget(self.email_line_edit, 2, 1)
        layout.addWidget(self.save_button, 3, 0)
        layout.addWidget(self.cancel_button, 3, 1)
        self.setLayout(layout)

        # Connect the save and cancel buttons to their respective functions
        self.save_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

    def get_name(self):
        return self.name_line_edit.text()

    def get_phone(self):
        return self.phone_line_edit.text()

    def get_email(self):
        return self.email_line_edit.text()
