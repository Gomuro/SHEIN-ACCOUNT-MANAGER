import sys
import json
import uuid
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit,
    QLabel, QMessageBox, QComboBox, QTextEdit
)
from PyQt6.QtCore import Qt
from GLOBAL import GLOBAL
from driver.driver import TwitterBotDriver
from proxy import Proxy
from sqlalchemy import create_engine, Column, String, Text
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()


class Account(Base):
    __tablename__ = 'accounts'
    uuid = Column(String, primary_key=True, default=str(uuid.uuid4()))
    account_name = Column(String, unique=True, nullable=False)
    proxy = Column(String, nullable=False)
    user_agent = Column(String, nullable=False)
    cookies = Column(Text, nullable=False)


engine = create_engine('sqlite:///accounts.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def show_message_box(message, title="Info", icon=QMessageBox.Icon.Information):
    msg_box = QMessageBox()
    msg_box.setIcon(icon)
    msg_box.setText(message)
    msg_box.setWindowTitle(title)
    msg_box.exec()


def login_and_retrieve_cookies(account_name, inner_proxy_string: str = None, user_agent: str = None):
    inner_proxy = Proxy.from_user_format_string(inner_proxy_string)

    try:
        new_driver = TwitterBotDriver(executable_path=GLOBAL.PATH.CHROMEDRIVER_PATH, proxy=inner_proxy,
                                      user_agent=user_agent, headless=False, window_size=(400, 900))
        new_driver.create_instance()
        new_driver.get('https://www.shein.com/')

        show_message_box("Please log in manually and press Enter when logged in...", "Login Required")
        input("Please log in manually and press Enter when logged in...")

        cookies = new_driver.get_cookies()
        cookies_json = json.dumps(cookies)

        new_account = Account(account_name=account_name, proxy=inner_proxy_string, user_agent=user_agent,
                              cookies=cookies_json)
        session.add(new_account)
        session.commit()

        new_driver.quit()
        show_message_box("Cookies saved.", "Success")
    except Exception as e:
        show_message_box(f"An error occurred: {e}", "Error", QMessageBox.Icon.Critical)
        new_driver.quit()


def open_account(account_name):
    account = session.query(Account).filter_by(account_name=account_name).first()
    if account:
        try:
            inner_proxy = Proxy.from_user_format_string(account.proxy)
            driver = TwitterBotDriver(executable_path=GLOBAL.PATH.CHROMEDRIVER_PATH, proxy=inner_proxy,
                                      user_agent=account.user_agent, headless=False, window_size=(400, 900))
            driver.create_instance()

            driver.get('https://www.shein.com/')

            cookies = json.loads(account.cookies)
            driver.delete_all_cookies()
            current_web_cookies = driver.get_cookies()
            for cookie in current_web_cookies:
                driver.delete_cookie(cookie['name'])
            for cookie in cookies:
                driver.add_cookie(cookie)

            driver.refresh()
            show_message_box(f"Logged in as {account_name},Please press Enter when done...", "Success")
            input("Press Enter to exit when done...")
            driver.quit()
        except Exception as e:
            show_message_box(f"An error occurred: {e}", "Error", QMessageBox.Icon.Critical)
            driver.quit()
    else:
        show_message_box("Account not found.", "Error", QMessageBox.Icon.Critical)


def updated_account_cookies(account_name):
    account = session.query(Account).filter_by(account_name=account_name).first()
    if account:
        try:
            driver = TwitterBotDriver(executable_path=GLOBAL.PATH.CHROMEDRIVER_PATH, proxy=account.proxy,
                                      user_agent=account.user_agent, headless=False, window_size=(400, 900))
            driver.create_instance()
            driver.get('https://www.shein.com/')
            show_message_box("Please log in manually and press Enter when logged in...", "Login Required")
            input("Please log in manually and press Enter when logged in...")

            cookies = driver.get_cookies()
            cookies_json = json.dumps(cookies)
            session.query(Account).filter_by(account_name=account_name).update({'cookies': cookies_json})
            session.commit()
            show_message_box("Cookies updated.", "Success")
            driver.quit()
        except Exception as e:
            show_message_box(f"An error occurred: {e}", "Error", QMessageBox.Icon.Critical)
            driver.quit()
    else:
        show_message_box("Account not found.", "Error", QMessageBox.Icon.Critical)


def updated_account(account_name, field, value):
    try:
        update_dict = {field: value}
        session.query(Account).filter_by(account_name=account_name).update(update_dict)
        session.commit()
        show_message_box(f"{field} updated.", "Success")
        if field in ['proxy', 'user_agent']:
            show_message_box("Now you need to log in again to apply the new settings and not be suspended by Shein.",
                             "Info")
            updated_account_cookies(account_name)
    except Exception as e:
        show_message_box(f"An error occurred: {e}", "Error", QMessageBox.Icon.Critical)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Account Manager")

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

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

        self.quit_button = QPushButton("Quit")
        self.quit_button.clicked.connect(self.close)
        self.layout.addWidget(self.quit_button)

    def add_account(self):
        self.account_form = AccountForm()
        self.account_form.show()

    def open_account(self):
        self.account_selector = AccountSelector()
        self.account_selector.account_selected.connect(open_account)
        self.account_selector.show()

    def update_account(self):
        self.account_selector = AccountSelector(update=True)
        self.account_selector.account_selected.connect(self.update_selected_account)
        self.account_selector.show()

    def update_account_cookies(self):
        self.account_selector = AccountSelector()
        self.account_selector.account_selected.connect(updated_account_cookies)
        self.account_selector.show()

    def update_selected_account(self, account_name):
        self.update_form = UpdateAccountForm(account_name)
        self.update_form.show()


class AccountForm(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Add New Account")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.account_name_label = QLabel("Account Name:")
        self.layout.addWidget(self.account_name_label)
        self.account_name_input = QLineEdit()
        self.layout.addWidget(self.account_name_input)

        self.proxy_label = QLabel("Proxy:")
        self.layout.addWidget(self.proxy_label)
        self.proxy_input = QLineEdit()
        self.layout.addWidget(self.proxy_input)

        self.user_agent_label = QLabel("User Agent:")
        self.layout.addWidget(self.user_agent_label)
        self.user_agent_input = QLineEdit()
        self.layout.addWidget(self.user_agent_input)

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit)
        self.layout.addWidget(self.submit_button)

    def submit(self):
        account_name = self.account_name_input.text()
        proxy = self.proxy_input.text()
        user_agent = self.user_agent_input.text()

        login_and_retrieve_cookies(account_name, proxy, user_agent)
        self.close()


class AccountSelector(QWidget):
    from PyQt6.QtCore import pyqtSignal
    account_selected = pyqtSignal(str)

    def __init__(self, update=False):
        super().__init__()

        self.setWindowTitle("Select Account")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.combo_box = QComboBox()
        self.layout.addWidget(self.combo_box)

        self.update = update

        accounts = session.query(Account).all()
        for account in accounts:
            self.combo_box.addItem(account.account_name)

        self.select_button = QPushButton("Select")
        self.select_button.clicked.connect(self.select_account)
        self.layout.addWidget(self.select_button)

    def select_account(self):
        account_name = self.combo_box.currentText()
        self.account_selected.emit(account_name)
        self.close()


class UpdateAccountForm(QWidget):
    def __init__(self, account_name):
        super().__init__()

        self.account_name = account_name

        self.setWindowTitle(f"Update Account: {account_name}")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.field_selector = QComboBox()
        self.field_selector.addItems(["proxy", "user_agent", "account_name"])
        self.layout.addWidget(self.field_selector)

        self.value_input = QLineEdit()
        self.layout.addWidget(self.value_input)

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit)
        self.layout.addWidget(self.submit_button)

    def submit(self):
        field = self.field_selector.currentText()
        value = self.value_input.text()
        updated_account(self.account_name, field, value)
        self.close()


def main():
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    import undetected_chromedriver as uc
    from selenium.webdriver.chrome.service import Service

    options = uc.ChromeOptions()
    driver = uc.Chrome(options=options)
    driver.get('https://www.shein.com/')
    print(driver.title)
    driver.quit()

