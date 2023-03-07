import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
)


class Phonebook(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # create labels and line edits for the name and phone number
        nameLabel = QLabel("Name:")
        self.nameLineEdit = QLineEdit()
        phoneLabel = QLabel("Phone Number:")
        self.phoneLineEdit = QLineEdit()

        # create buttons for adding, deleting, editing, and sorting contacts
        addButton = QPushButton("Add")
        addButton.clicked.connect(self.addContact)
        deleteButton = QPushButton("Delete")
        deleteButton.clicked.connect(self.deleteContact)
        editButton = QPushButton("Edit")
        editButton.clicked.connect(self.editContact)
        sortButton = QPushButton("Sort")
        sortButton.clicked.connect(self.sortContacts)

        # create a table to display the contacts
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Name", "Phone Number"])

        # create a horizontal box layout for the name and phone number
        hbox = QHBoxLayout()
        hbox.addWidget(nameLabel)
        hbox.addWidget(self.nameLineEdit)
        hbox.addWidget(phoneLabel)
        hbox.addWidget(self.phoneLineEdit)

        # create a horizontal box layout for the buttons
        buttonBox = QHBoxLayout()
        buttonBox.addWidget(addButton)
        buttonBox.addWidget(deleteButton)
        buttonBox.addWidget(editButton)
        buttonBox.addWidget(sortButton)

        # create a vertical box layout for the name/phone number layout, the table, and the button layout
        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addWidget(self.table)
        vbox.addLayout(buttonBox)

        self.setLayout(vbox)

        self.setGeometry(300, 300, 500, 400)
        self.setWindowTitle("Phonebook")
        self.show()

    def addContact(self):
        name = self.nameLineEdit.text()
        phone = self.phoneLineEdit.text()

        if name and phone:
            rowPosition = self.table.rowCount()
            self.table.insertRow(rowPosition)
            self.table.setItem(rowPosition, 0, QTableWidgetItem(name))
            self.table.setItem(rowPosition, 1, QTableWidgetItem(phone))
            self.nameLineEdit.setText("")
            self.phoneLineEdit.setText("")
        else:
            QMessageBox.warning(
                self, "Warning", "Please enter both name and phone number."
            )

    def deleteContact(self):
        selected = self.table.currentRow()

        if selected != -1:
            self.table.removeRow(selected)
        else:
            QMessageBox.warning(self, "Warning", "Please select a contact to delete.")

    def editContact(self):
        selected = self.table.currentRow()

        if selected != -1:
            name, phone = (
                self.table.item(selected, 0).text(),
                self.table.item(selected, 1).text(),
            )
            self.nameLineEdit.setText(name)
            self.phoneLineEdit.setText(phone)
            self.table.removeRow(selected)
        else:
            QMessageBox.warning(self, "Warning", "Please select a contact to edit.")

    def sortContacts(self):
        self.table.sortItems(0, Qt.AscendingOrder)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    phonebook = Phonebook()
    sys.exit(app.exec_())
