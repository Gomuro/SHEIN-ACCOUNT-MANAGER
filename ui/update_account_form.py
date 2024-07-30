from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QComboBox, QLineEdit, QPushButton, QLabel, QMessageBox
from helpers import updated_account
from proxy import Proxy, EmptyProxy


class UpdateAccountForm(QWidget):
    def __init__(self, account_name):
        super().__init__()

        self.account_name = account_name

        self.setWindowTitle(f"Update Account: {account_name}")
        self.resize(300, 200)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Helper function to create and add QLabel
        self.explain_label = QLabel("Explain:")
        self.explain_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.explain_label)

        self.explain_label = QLabel("1. choose field\n"
                                    "2. enter new value\n"
                                    "3. click submit\n"
                                    "P.S. If you update proxy or user agent, it will update the cookies too.\n"
                                    "Which means you will need to log in again.\n"
                                    "We Doing it for you not get suspicious accounts.\n"
                                    "Also, do not change the proxy or user agent, very often to not get suspicious accounts.")
        self.layout.addWidget(self.explain_label)

        # Adding field selector
        self.field_selector = QComboBox()
        self.field_selector.addItems(["proxy", "user_agent", "account_name"])
        self.layout.addWidget(self.field_selector)

        # Adding input field for the new value
        self.value_input = QLineEdit()
        self.layout.addWidget(self.value_input)
        self.value_input.textChanged.connect(self.validate_input)

        # Adding submit button
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit)
        self.submit_button.setEnabled(False)  # Disable submit button initially
        self.layout.addWidget(self.submit_button)

    def validate_input(self):
        if self.value_input.text():
            self.submit_button.setEnabled(True)

    def submit(self):
        field = self.field_selector.currentText()
        value = self.value_input.text()

        if field == "account_name":
            updated_account(self.account_name, field, value)
            self.close()
            return
        elif field == "proxy":
            test_value = Proxy.from_user_format_string(value)
            # if the proxy has not EmptyProxy object then save
            if not isinstance(test_value, EmptyProxy):
                updated_account(self.account_name, field, value)
                self.close()
            else:
                QMessageBox.warning(self, "Invalid Input", "Please enter valid proxy.")
                return

        elif field == "user_agent":
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

            if not valid_user_agent(self, value):
                QMessageBox.warning(self, "Invalid Input", "Please enter valid user agent.")
                return
            updated_account(self.account_name, field, value)
            self.close()
