from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import mysql.connector
import sys

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="phonebook",
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Phonebook")
        self.setFixedSize(600, 600)
        self.init_ui()

    def init_ui(self):
        # Create the table widget for contacts
        self.contacts_table = QTableWidget(self)
        self.contacts_table.setGeometry(10, 70, 480, 320)
        self.contacts_table.setColumnCount(3)
        self.contacts_table.setHorizontalHeaderLabels(["Name", "Phone", "Email"])
        self.contacts_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.contacts_table.verticalHeader().setVisible(False)
        self.contacts_table.hide()

        # Create labels and input fields for name, phone and email
        self.name_label = QLabel("Name:", self)
        self.name_label.setGeometry(10, 10, 80, 30)
        self.name_input = QLineEdit(self)
        self.name_input.setGeometry(70, 10, 120, 30)

        self.phone_label = QLabel("Phone:", self)
        self.phone_label.setGeometry(199, 10, 80, 30)
        self.phone_input = QLineEdit(self)
        self.phone_input.setGeometry(240, 10, 170, 30)

        self.email_label = QLabel("Email:", self)
        self.email_label.setGeometry(10, 40, 80, 30)
        self.email_input = QLineEdit(self)
        self.email_input.setGeometry(70, 40, 340, 30)

        # Create buttons for adding, deleting, editing and sorting contacts
        self.add_button = QPushButton("Add", self)
        self.add_button.setGeometry(520, 10, 80, 30)
        self.add_button.clicked.connect(self.add_contact)

        self.delete_button = QPushButton("Delete", self)
        self.delete_button.setGeometry(520, 40, 80, 30)
        self.delete_button.clicked.connect(self.delete_contact)

        self.edit_button = QPushButton("Edit", self)
        self.edit_button.setGeometry(450, 10, 80, 30)
        self.edit_button.clicked.connect(self.edit_contact)

        self.sort_button = QPushButton("Sort", self)
        self.sort_button.setGeometry(450, 40, 80, 30)
        self.sort_button.clicked.connect(self.sort_contacts)

        # Create checkbox for showing/hiding the contacts table
        self.show_contacts_checkbox = QCheckBox("Show Contacts", self)
        self.show_contacts_checkbox.setGeometry(10, 400, 120, 20)
        self.show_contacts_checkbox.stateChanged.connect(self.toggle_contacts_table)

        # Create button for refreshing the contacts table
        self.refresh_button = QPushButton("Refresh", self)
        self.refresh_button.setGeometry(400, 400, 90, 20)
        self.refresh_button.clicked.connect(self.show_all_contacts)

        # Add all components to a vertical layout
        layout = QVBoxLayout()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.phone_label)
        layout.addWidget(self.phone_input)
        layout.addWidget(self.email_label)
        layout.addWidget(self.email_input)
        layout.addWidget(self.add_button)
        layout.addWidget(self.delete_button)
        layout.addWidget(self.edit_button)
        layout.addWidget(self.sort_button)
        layout.addWidget(self.show_contacts_checkbox)
        layout.addWidget(self.refresh_button)
        layout.addWidget(self.contacts_table)
        layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(layout)
        self.show_all_contacts()

    def show_all_contacts(self):
        mycursor = mydb.cursor()
        sql = "SELECT * FROM contacts"
        mycursor.execute(sql)
        result = mycursor.fetchall()

        self.contacts_table.setRowCount(0)

        if result:
            for row_number, row_data in enumerate(result):
                self.contacts_table.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.contacts_table.setItem(
                        row_number, column_number, QTableWidgetItem(str(data))
                    )

    def add_contact(self):
        name = self.name_input.text()
        phone = self.phone_input.text()
        email = self.email_input.text()

        if name and phone and email:
            mycursor = mydb.cursor()
            sql = "INSERT INTO contacts (name, phone, email) VALUES (%s, %s, %s)"
            val = (name, phone, email)
            mycursor.execute(sql, val)
            mydb.commit()
            self.show_all_contacts()
            self.name_input.setText("")
            self.phone_input.setText("")
            self.email_input.setText("")
        else:
            QMessageBox.warning(self, "Error", "Please fill in all fields.")

    def delete_contact(self):
        selected_rows = self.contacts_table.selectedItems()

        if selected_rows:
            selected_name = selected_rows[0].text()
            mycursor = mydb.cursor()
            sql = "DELETE FROM contacts WHERE name = %s"
            val = (selected_name,)
            mycursor.execute(sql, val)
            mydb.commit()
            self.show_all_contacts()
        else:
            QMessageBox.warning(self, "Error", "Please select a contact to delete.")

    def edit_contact(self):
        selected_rows = self.contacts_table.selectedItems()

        if selected_rows:
            selected_name = selected_rows[0].text()
            mycursor = mydb.cursor()
            sql = "SELECT * FROM contacts WHERE name = %s"
            val = (selected_name,)
            mycursor.execute(sql, val)
            result = mycursor.fetchone()

            if result:
                name, phone, email = result
                self.name_input.setText(name)
                self.phone_input.setText(phone)
                self.email_input.setText(email)

                reply = QMessageBox.question(
                    self,
                    "Edit Contact",
                    "Do you want to save the changes?",
                    QMessageBox.Yes | QMessageBox.No,
                )
                if reply == QMessageBox.Yes:
                    name = self.name_input.text()
                    phone = self.phone_input.text()
                    email = self.email_input.text()
                    sql = "UPDATE contacts SET phone = %s, email = %s WHERE name = %s"
                    val = (phone, email, selected_name)
                    mycursor.execute(sql, val)
                    mydb.commit()
                    self.show_all_contacts()
                    self.name_input.setText("")
                    self.phone_input.setText("")
                    self.email_input.setText("")
            else:
                QMessageBox.warning(
                    self, "Error", "An error occurred while retrieving the contact."
                )
        else:
            QMessageBox.warning(self, "Error", "Please select a contact to edit.")

    def sort_contacts(self):
        self.contacts_table.setSortingEnabled(True)
        self.contacts_table.sortByColumn(0, Qt.AscendingOrder)

    def toggle_contacts_table(self):
        if self.show_contacts_checkbox.isChecked():
            self.contacts_table.show()
        else:
            self.contacts_table.hide()

    class AddContactDialog(QDialog):
        def init(self):
            super().init()
            self.setWindowTitle("Add Contact")
            self.setFixedSize(300, 200)

            self.name_label = QLabel("Name:", self)
            self.name_label.setGeometry(10, 10, 80, 30)
            self.name_input = QLineEdit(self)
            self.name_input.setGeometry(100, 10, 180, 30)

            self.phone_label = QLabel("Phone:", self)
            self.phone_label.setGeometry(10, 50, 80, 30)
            self.phone_input = QLineEdit(self)
            self.phone_input.setGeometry(100, 50, 180, 30)

            self.email_label = QLabel("Email:", self)
            self.email_label.setGeometry(10, 90, 80, 30)
            self.email_input = QLineEdit(self)
            self.email_input.setGeometry(100, 90, 180, 30)

            self.ok_button = QPushButton("OK", self)
            self.ok_button.setGeometry(70, 140, 60, 30)
            self.ok_button.clicked.connect(self.accept)

            self.cancel_button = QPushButton("Cancel", self)
            self.cancel_button.setGeometry(170, 140, 60, 30)
            self.cancel_button.clicked.connect(self.reject)

            try:
                mycursor.execute(sql, val)
                mydb.commit()
                self.show_all_contacts()
                self.name_input.setText("")
                self.phone_input.setText("")
                self.email_input.setText("")
            except mysql.connector.Error as error:
                print("Error inserting contact: {}".format(error))

    def delete_contact(self):
        selected_rows = self.contacts_table.selectedIndexes()
        if selected_rows:
            indexes = [index.row() for index in selected_rows]
            names = [self.contacts_table.item(index, 0).text() for index in indexes]

            message_box = QMessageBox.question(
                self,
                "Delete Contacts",
                "Are you sure you want to delete the selected contacts?",
                QMessageBox.Yes | QMessageBox.No,
            )

            if message_box == QMessageBox.Yes:
                mycursor = mydb.cursor()
                sql = "DELETE FROM contacts WHERE name IN ({})".format(
                    ", ".join(["%s"] * len(names))
                )
                mycursor.execute(sql, names)
                mydb.commit()
                self.show_all_contacts()

    def edit_contact(self):
        selected_rows = self.contacts_table.selectedIndexes()
        if selected_rows:
            row_index = selected_rows[0].row()
            name = self.contacts_table.item(row_index, 0).text()
            phone = self.contacts_table.item(row_index, 1).text()
            email = self.contacts_table.item(row_index, 2).text()

            edit_dialog = EditContactDialog(name, phone, email)
            if edit_dialog.exec_():
                new_name = edit_dialog.name_input.text()
                new_phone = edit_dialog.phone_input.text()
                new_email = edit_dialog.email_input.text()

                mycursor = mydb.cursor()
                sql = "UPDATE contacts SET name = %s, phone = %s, email = %s WHERE name = %s"
                val = (new_name, new_phone, new_email, name)

                try:
                    mycursor.execute(sql, val)
                    mydb.commit()
                    self.show_all_contacts()
                except mysql.connector.Error as error:
                    print("Error updating contact: {}".format(error))

    def sort_contacts(self):
        self.contacts_table.sortItems(0)

    def toggle_contacts_table(self):
        if self.show_contacts_checkbox.isChecked():
            self.contacts_table.show()
        else:
            self.contacts_table.hide()


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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
