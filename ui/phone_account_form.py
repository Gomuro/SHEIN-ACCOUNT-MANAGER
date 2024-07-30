from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QMessageBox, QVBoxLayout


from helpers import create_and_save_phone_emulator
from proxy import Proxy, EmptyProxy


class PhoneAccountForm(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Add new phone account")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.resize(300, 200)

        self.explain_label = QLabel("How to use it?")
        self.explain_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.explain_label)

        self.explain_label = QLabel("1. choose account name\n"
                                    "2. choose proxy\n"
                                    "example: 111.222.333.444:8080\n"
                                    "be sure froxy is working because if it is not working\n"
                                    "you will not be able to login\n"
                                    "and let's go")
        self.layout.addWidget(self.explain_label)

        self.account_name_label = QLabel("Account Name:")
        self.layout.addWidget(self.account_name_label)
        self.account_name_input = QLineEdit()
        self.layout.addWidget(self.account_name_input)

        self.proxy_label = QLabel("Proxy:")
        self.layout.addWidget(self.proxy_label)
        self.proxy_input = QLineEdit()
        self.layout.addWidget(self.proxy_input)

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit)
        self.layout.addWidget(self.submit_button)

    def submit(self):
        account_name = self.account_name_input.text()
        proxy = self.proxy_input.text()

        if not self.valid_proxy(proxy):
            QMessageBox.warning(self, "Invalid Proxy", "Please enter a valid proxy.")
            return
        create_and_save_phone_emulator(account_name=account_name, proxy=Proxy.from_user_format_string(proxy))
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