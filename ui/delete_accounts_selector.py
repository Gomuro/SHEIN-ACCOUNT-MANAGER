from PyQt6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QPushButton
from PyQt6.QtCore import pyqtSignal
from sqlalchemy.orm import sessionmaker
from database import engine, Account

Session = sessionmaker(bind=engine)
session = Session()

class DeleteAccountsSelector(QWidget):
    accounts_selected = pyqtSignal(list)

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Select Accounts to Delete")
        self.resize(400, 300)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        self.layout.addWidget(self.list_widget)

        # Populate the list widget with existing account names
        accounts = session.query(Account).all()
        sorted_accounts = sorted(accounts, key=lambda account: account.account_name)
        for account in sorted_accounts:
            self.list_widget.addItem(account.account_name)

        self.delete_button = QPushButton("Delete Selected Accounts")
        self.delete_button.clicked.connect(self.delete_accounts)
        self.layout.addWidget(self.delete_button)

    def delete_accounts(self):
        """Emit the list of selected account names and close the selector."""
        selected_items = self.list_widget.selectedItems()
        account_names = [item.text() for item in selected_items]
        self.accounts_selected.emit(account_names)
        self.close()
