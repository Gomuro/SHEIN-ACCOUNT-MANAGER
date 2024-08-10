import uuid
from typing import List

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox

from proxy import EmptyProxy
from ui.account_form import AccountForm
from ui.account_selector import AccountSelector
from ui.phone_account_form import PhoneAccountForm
from ui.phone_account_selector import PhoneAccountSelector
from ui.update_account_form import UpdateAccountForm
from ui.delete_accounts_selector import DeleteAccountsSelector
from helpers import open_account, updated_account_cookies, delete_accounts, create_and_save_phone_emulator
from database import session, Phone_emulator
from utils.terminal import Terminal


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Shein Account Manager")
        self.resize(600, 400)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.welcome_label = QLabel("Welcome to the Shein Account Manager!")
        self.welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.welcome_label.setWordWrap(True)
        self.welcome_label.setStyleSheet("font-size: 24px;")
        self.layout.addWidget(self.welcome_label)

        self.add_account_button = QPushButton("Add New Account")
        self.add_account_button.clicked.connect(self.add_account)
        self.layout.addWidget(self.add_account_button)

        self.open_account_button = QPushButton("Open Existing Account")
        self.open_account_button.clicked.connect(self.open_account)
        self.layout.addWidget(self.open_account_button)

        self.update_account_button = QPushButton("Update Account Credentials")
        self.update_account_button.clicked.connect(self.update_account)
        self.layout.addWidget(self.update_account_button)

        self.update_cookies_button = QPushButton("Update Account Cookies")
        self.update_cookies_button.clicked.connect(self.update_account_cookies)
        self.layout.addWidget(self.update_cookies_button)

        self.delete_accounts_button = QPushButton("Delete Selected Accounts")
        self.delete_accounts_button.clicked.connect(self.delete_accounts)
        self.layout.addWidget(self.delete_accounts_button)

        self.create_emulator_button = QPushButton("Create New Phone Emulator")
        self.create_emulator_button.clicked.connect(self.create_and_save_emulator)
        self.layout.addWidget(self.create_emulator_button)

        self.open_emulator_button = QPushButton("Open Phone Emulator")
        self.open_emulator_button.clicked.connect(self.open_emulator)
        self.layout.addWidget(self.open_emulator_button)

        self.update_phone_emulator_button = QPushButton("Update Phone Emulator")
        self.update_phone_emulator_button.clicked.connect(self.update_phone_emulator_select)
        self.layout.addWidget(self.update_phone_emulator_button)

        self.delete_phone_emulator_button = QPushButton("Delete Phone Emulator")
        self.delete_phone_emulator_button.clicked.connect(self.delete_phone_emulator_select)
        self.layout.addWidget(self.delete_phone_emulator_button)

        self.quit_button = QPushButton("Quit")
        self.quit_button.clicked.connect(self.close)
        self.layout.addWidget(self.quit_button)

        """
        initialization of database phone emulator data table
        """

        self.init_phone_emulator_table()

        """
            Initialization of forms widgets and selectors
        """
        self.account_form = AccountForm()
        self.account_selector = AccountSelector()
        self.delete_selector = DeleteAccountsSelector()
        self.phone_account_form = PhoneAccountForm()
        self.phone_account_selector = PhoneAccountSelector()

    def add_account(self):
        """Open the form to add a new account."""
        self.account_form.show()

    def open_account(self):
        """Open the account selector to choose an existing account."""
        self.account_selector.account_selected.connect(open_account)
        self.account_selector.show()

    def update_account(self):
        """Open the account selector to choose an account to update its credentials."""
        self.account_selector = AccountSelector(update=True)
        self.account_selector.account_selected.connect(self.update_selected_account)
        self.account_selector.show()

    def update_account_cookies(self):
        """Open the account selector to choose an account to update its cookies."""
        self.account_selector = AccountSelector()
        self.account_selector.account_selected.connect(updated_account_cookies)
        self.account_selector.show()

    def delete_accounts(self):
        """Open the selector to choose accounts to delete."""
        self.delete_selector.accounts_selected.connect(self.confirm_delete_accounts)
        self.delete_selector.show()

    def update_selected_account(self, account_name):
        """Open the form to update the selected account's details."""
        self.update_form = UpdateAccountForm(account_name)
        self.update_form.show()

    def confirm_delete_accounts(self, account_names):
        """Prompt the user to confirm deletion of multiple accounts."""
        if not account_names:
            QMessageBox.warning(self, "No Accounts Selected", "No accounts were selected for deletion.")
            return

        reply = QMessageBox.question(
            self,
            'Confirm Deletion',
            f"Are you sure you want to delete the following accounts:\n\n{', '.join(account_names)}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            delete_accounts(account_names)
            QMessageBox.information(self, "Accounts Deleted", "Selected accounts have been deleted.")

    def create_and_save_emulator(self):

        self.phone_account_form.show()

    def open_emulator(self):
        self.phone_account_selector.phone_account_selected.connect(self.open_phone_emulator)
        self.phone_account_selector.show()

    def open_phone_emulator(self, phone_account):
        self.phone_account_selector.close()

    def update_phone_emulator_select(self):
        self.phone_account_selector.phone_account_selected.connect(self.update_phone_emulator)
        self.phone_account_selector.show()

    def update_phone_emulator(self, phone_account):
        self.phone_account_selector.close()

    def delete_phone_emulator_select(self):
        self.phone_account_selector.phone_account_selected.connect(self.delete_phone_emulator)
        self.phone_account_selector.show()

    def delete_phone_emulator(self, phone_account):
        self.phone_account_selector.close()

    def init_phone_emulator_table(self):
        """Initialize the phone emulator table by adding new emulator data to the database."""
        phone_emulators = self.get_phone_emulators()
        existing_emulator_avd_names = {
            emulator.avd_name for emulator in session.query(Phone_emulator).all()
        }

        new_emulators = [
            emulator for emulator in phone_emulators
            if emulator not in existing_emulator_avd_names
        ]

        new_emulator_data = [
            Phone_emulator(
                id=str(uuid.uuid4()),
                proxy=EmptyProxy.to_user_format_string(EmptyProxy()),
                avd_name=emulator,
                account_name=emulator
            )
            for emulator in new_emulators
        ]

        if new_emulator_data:
            session.add_all(new_emulator_data)
            session.commit()

    @staticmethod
    def get_phone_emulators() -> List[str]:
        """Return a list of initialized emulator names."""
        terminal = Terminal()
        return terminal.list_initialized_emulators()
