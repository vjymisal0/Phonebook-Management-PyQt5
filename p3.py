from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import mysql.connector


class PhonebookWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Phonebook")
        self.resize(800, 600)
        self.setup_ui()

        self.contacts = []
        self.load_contacts()

    def setup_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # search bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search Contacts")
        self.search_bar.textChanged.connect(self.filter_contacts)
        self.layout.addWidget(self.search_bar)

        # contacts table
        self.contacts_table = QTableWidget()
        self.contacts_table.setSortingEnabled(True)
        self.contacts_table.setColumnCount(3)
        self.contacts_table.setHorizontalHeaderLabels(["Name", "Phone", "Email"])
        self.contacts_table.horizontalHeader().setStretchLastSection(True)
        self.layout.addWidget(self.contacts_table)

        # toolbar
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        # add contact
        add_contact_action = QAction(
            QIcon("icons/add_contact.png"), "Add Contact", self
        )
        add_contact_action.triggered.connect(self.add_contact)
        toolbar.addAction(add_contact_action)

        # delete contact
        delete_contact_action = QAction(
            QIcon("icons/delete_contact.png"), "Delete Contact", self
        )
        delete_contact_action.triggered.connect(self.delete_contact)
        toolbar.addAction(delete_contact_action)

        # edit contact
        edit_contact_action = QAction(
            QIcon("icons/edit_contact.png"), "Edit Contact", self
        )
        edit_contact_action.triggered.connect(self.edit_contact)
        toolbar.addAction(edit_contact_action)

        # refresh contacts
        refresh_contacts_action = QAction(
            QIcon("icons/refresh_contacts.png"), "Refresh Contacts", self
        )
        refresh_contacts_action.triggered.connect(self.load_contacts)
        toolbar.addAction(refresh_contacts_action)

        self.show()

    def load_contacts(self):
        self.contacts_table.setRowCount(0)
        self.contacts.clear()

        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="phonebook",
        )

        mycursor = mydb.cursor()
        mycursor.execute("SELECT name, phone, email FROM contacts")
        result = mycursor.fetchall()

        if result:
            for row in result:
                self.contacts.append(row)
                row_position = self.contacts_table.rowCount()
                self.contacts_table.insertRow(row_position)

                for column_number, data in enumerate(row):
                    self.contacts_table.setItem(
                        row_position, column_number, QTableWidgetItem(str(data))
                    )

        mycursor.close()
        mydb.close()

    def add_contact(self):
        add_contact_dialog = AddContactDialog()
        result = add_contact_dialog.exec_()
        if result == QDialog.Accepted:
            name = add_contact_dialog.name_input.text()
            phone = add_contact_dialog.phone_input.text()
            email = add_contact_dialog.email_input.text()

            mydb = mysql
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

    def toggle_contacts_table(self, state):
        if state == Qt.Checked:
            self.contacts_table.show()
        else:
            self.contacts_table.hide()
if name == "main":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())