from PyQt6.QtWidgets import QWidget, QVBoxLayout, QComboBox, QPushButton
from PyQt6.QtCore import pyqtSignal
from database import session, Account

class AccountSelector(QWidget):
    account_selected = pyqtSignal(str)

    def __init__(self, update=False):
        super().__init__()

        self.setWindowTitle("Select Account")
        self.resize(300, 200)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.combo_box = QComboBox()
        self.layout.addWidget(self.combo_box)

        self.update = update

        accounts = session.query(Account).all()
        sorted_accounts = sorted(accounts, key=lambda account: account.account_name)
        for account in sorted_accounts:
            self.combo_box.addItem(account.account_name)

        self.select_button = QPushButton("Select")
        self.select_button.clicked.connect(self.select_account)
        self.layout.addWidget(self.select_button)

    def select_account(self):
        account_name = self.combo_box.currentText()
        self.account_selected.emit(account_name)
        self.close()
