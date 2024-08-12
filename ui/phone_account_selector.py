from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QComboBox, QLabel

from database import Phone_emulator, session


class PhoneAccountSelector(QWidget):
    phone_account_selected = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Select Phone Account")
        self.resize(300, 200)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.label = QLabel("Select Phone Account:")
        self.layout.addWidget(self.label)

        self.comboBox = QComboBox()
        self.layout.addWidget(self.comboBox)

        # Populate the combo box with existing phone account names
        accounts = session.query(Phone_emulator).all()
        sorted_accounts = sorted(accounts, key=lambda account: account.account_name)
        for account in sorted_accounts:
            self.comboBox.addItem(account.account_name)

        self.select_button = QPushButton("Select")
        self.select_button.clicked.connect(self.select_account)
        self.layout.addWidget(self.select_button)

    def select_account(self):
        selected_account_name = self.comboBox.currentText()
        self.phone_account_selected.emit(selected_account_name)

    def update(self):
        self.comboBox.clear()
        accounts = session.query(Phone_emulator).all()
        sorted_accounts = sorted(accounts, key=lambda account: account.account_name)
        for account in sorted_accounts:
            self.comboBox.addItem(account.account_name)
