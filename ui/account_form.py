from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit,
    QLabel, QTextEdit, QMessageBox, QComboBox, QCheckBox
)
from PyQt6.QtCore import Qt

from helpers import login_and_retrieve_cookies, Account, session
from proxy import Proxy, EmptyProxy


class AccountForm(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Add New Account")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.resize(300, 200)

        self.explain_label = QLabel("Explain:")
        self.explain_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.explain_label)

        self.explain_label = QLabel("1. choose account name\n"
                                    "(recommended to use your Shein username or email address)\n"
                                    "2. choose proxy\n example: 111.222.333.444:8080\n"
                                    "be sure froxy is working because if it is not working\n"
                                    "you will not be able to login\n"
                                    "and will get an error message in browser\n"
                                    "3. choose user agent\n"
                                    "example: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.142.86 Safari/537.36\n"
                                    "PS: Recommendation to use real email and phone number, not temp.\n"
                                    "for that you can use ProtonMail or other email providers.\n")
        self.layout.addWidget(self.explain_label)


        self.account_name_label = QLabel("Account Name:")
        self.layout.addWidget(self.account_name_label)
        self.account_name_input = QLineEdit()
        self.layout.addWidget(self.account_name_input)

        self.proxy_label = QLabel("Proxy:")
        self.layout.addWidget(self.proxy_label)
        self.proxy_input = QLineEdit()
        self.layout.addWidget(self.proxy_input)
        self.proxy_input.textChanged.connect(self.validate_inputs)

        self.user_agent_label = QLabel("User Agent:")
        self.layout.addWidget(self.user_agent_label)
        self.user_agent_input = QLineEdit()
        self.layout.addWidget(self.user_agent_input)
        self.user_agent_input.textChanged.connect(self.validate_inputs)

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit)
        self.submit_button.setEnabled(False)  # Disable submit button initially
        self.layout.addWidget(self.submit_button)

        self.account_name_input.textChanged.connect(self.validate_inputs)
        self.proxy_input.textChanged.connect(self.validate_inputs)
        self.user_agent_input.textChanged.connect(self.validate_inputs)

    def validate_inputs(self):
        account_name = self.account_name_input.text().strip()
        proxy = self.proxy_input.text().strip()
        user_agent = self.user_agent_input.text().strip()

        if account_name and proxy and user_agent:
            self.submit_button.setEnabled(True)
        else:
            self.submit_button.setEnabled(False)

    def submit(self):
        account_name = self.account_name_input.text()
        proxy = self.proxy_input.text()
        user_agent = self.user_agent_input.text()

        accounts = session.query(Account).all()
        for account in accounts:
            if account.account_name == account_name:
                QMessageBox.warning(self, "Duplicate Account Name", "Account name already exists.")
                return

        # Assume valid_proxy and valid_user_agent are functions to validate the proxy and user agent
        if not self.valid_user_agent(user_agent):
            QMessageBox.warning(self, "Invalid User Agent", "Please enter a valid user agent.")
        elif not self.valid_proxy(proxy):
            QMessageBox.warning(self, "Invalid Proxy", "Please enter a valid proxy.")
        else:
            login_and_retrieve_cookies(account_name, proxy, user_agent)
            self.close()

    def valid_proxy(self, proxy):
        # proxy validation logic here
        if proxy == "":
            return False
        test_value = Proxy.from_user_format_string(proxy)
        # if the proxy has not EmptyProxy object then save
        if not isinstance(test_value, EmptyProxy):
            return True
        else:
            return False

    def valid_user_agent(self, user_agent):
        # user agent validation logic here
        import re
        if user_agent == "":
            return False
        if not user_agent:
            return False
        # pattern : /\((?<info>.*?)\)(\s|$)|(?<name>.*?)\/(?<version>.*?)(\s|$)/gm
        pattern = r"\((?P<info>.*?)\)(\s|$)|(?P<name>.*?)\/(?P<version>.*?)(\s|$)"
        if not re.match(pattern, user_agent):
            return False
        return True
