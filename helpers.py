import json
import uuid

import selenium

from GLOBAL import GLOBAL
from driver.driver import TwitterBotDriver
from emulator_setup.setup_emulator import AndroidEmulatorManager
from proxy import Proxy, EmptyProxy
from sqlalchemy import create_engine, Column, String, Text
from sqlalchemy.orm import sessionmaker, declarative_base
from PyQt6.QtWidgets import QMessageBox

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


def login_and_retrieve_cookies(account_name, inner_proxy_string: str = None, user_agent: str = None):
    inner_proxy = Proxy.from_user_format_string(inner_proxy_string)
    new_driver = TwitterBotDriver(executable_path=GLOBAL.PATH.CHROMEDRIVER_PATH, proxy=inner_proxy,
                                  user_agent=user_agent, headless=False, window_size=(400, 900))
    try:

        new_driver.create_instance()
        new_driver.get('https://www.shein.com/')

        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setText("Please log in manually and press OK when done.")
        msg_box.setWindowTitle("Manual Login Required")
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()

        cookies = new_driver.get_cookies()
        cookies_json = json.dumps(cookies)

        new_account = Account(account_name=account_name, proxy=inner_proxy_string, user_agent=user_agent,
                              cookies=cookies_json)
        session.add(new_account)
        session.commit()

        new_driver.quit()
        QMessageBox.information(None, "Success", "Cookies saved.")
    except selenium.common.exceptions.NoSuchWindowException as e:
        QMessageBox.critical(None, "Error", "You closed the browser manually. app will close.")
        new_driver.quit()
    except Exception as e:
        if 'unable to connect' in str(e).lower():
            QMessageBox.critical(None, "Error",
                                 "Failed to connect to the internet. Please check your internet connection.")
        elif 'no such window' in str(e).lower():
            QMessageBox.critical(None, "Error", "You closed the browser manually. app will close.")
        else:
            QMessageBox.critical(None, "Error", f"An error occurred: {e}")

        new_driver.quit()


def open_account(account_name):
    account = session.query(Account).filter_by(account_name=account_name).first()
    if account:
        inner_proxy = Proxy.from_user_format_string(account.proxy)
        driver = TwitterBotDriver(executable_path=GLOBAL.PATH.CHROMEDRIVER_PATH, proxy=inner_proxy,
                                  user_agent=account.user_agent, headless=False, window_size=(400, 900))
        try:
            driver.create_instance()
            driver.get('https://www.shein.com/')

            cookies = json.loads(account.cookies)
            driver.delete_all_cookies()
            for cookie in cookies:
                driver.add_cookie(cookie)

            driver.refresh()

            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Information)
            msg_box.setText(f"Press OK to exit: Logged in as {account_name}.")
            msg_box.setWindowTitle(f"Success Logged In As {account_name}")
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg_box.exec()

            driver.quit()
        except selenium.common.exceptions.NoSuchWindowException as e:
            QMessageBox.critical(None, "Error", "You closed the browser manually. app will close.")
            driver.quit()
        except Exception as e:
            if 'unable to connect' in str(e).lower():
                QMessageBox.critical(None, "Error",
                                     "Failed to connect to the internet. Please check your internet connection.")
            elif 'no such window' in str(e).lower():
                QMessageBox.critical(None, "Error", "You closed the browser manually. app will close.")
            else:
                QMessageBox.critical(None, "Error", f"An error occurred: {e}")

            driver.quit()
    else:
        QMessageBox.critical(None, "Error", "Account not found.")


def updated_account_cookies(account_name):
    account = session.query(Account).filter_by(account_name=account_name).first()
    if account:
        driver = TwitterBotDriver(executable_path=GLOBAL.PATH.CHROMEDRIVER_PATH, proxy=account.proxy,
                                  user_agent=account.user_agent, headless=False, window_size=(400, 900))
        try:
            driver.create_instance()
            driver.get('https://www.shein.com/')

            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Information)
            msg_box.setText("Please log in manually and press OK when done.")
            msg_box.setWindowTitle("Manual Login Required")
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg_box.exec()

            cookies = driver.get_cookies()
            cookies_json = json.dumps(cookies)
            session.query(Account).filter_by(account_name=account_name).update({'cookies': cookies_json})
            session.commit()

            QMessageBox.information(None, "Success", "Cookies updated.")
            driver.quit()
        except selenium.common.exceptions.NoSuchWindowException as e:
            QMessageBox.critical(None, "Error", "You closed the browser manually. app will close.")
            driver.quit()
        except Exception as e:
            if 'unable to connect' in str(e).lower():
                QMessageBox.critical(None, "Error",
                                     "Failed to connect to the internet. Please check your internet connection.")
            elif 'no such window' in str(e).lower():
                QMessageBox.critical(None, "Error", "You closed the browser manually. app will close.")
            else:
                QMessageBox.critical(None, "Error", f"An error occurred: {e}")

            driver.quit()
    else:
        QMessageBox.critical(None, "Error", "Account not found.")


def updated_account(account_name, field, value):
    update_dict = {field: value}
    session.query(Account).filter_by(account_name=account_name).update(update_dict)
    session.commit()
    QMessageBox.information(None, "Success", f"{field.capitalize()} updated.")
    if field in ['proxy', 'user_agent']:
        updated_account_cookies(account_name)


def delete_accounts(account_names):
    """Delete multiple accounts from the database."""
    for account_name in account_names:
        account = session.query(Account).filter_by(account_name=account_name).first()
        if account:
            session.delete(account)
            QMessageBox.information(None, "Success", f"Account {account_name} deleted.")
        else:
            QMessageBox.critical(None, "Error", f"Account {account_name} not found.")
    session.commit()


def create_and_save_phone_emulator(account_name, avd_name='Pixel_3a_API_31', proxy: Proxy | EmptyProxy = EmptyProxy()):
    emulator = AndroidEmulatorManager(account_name, avd_name, proxy)
    result = emulator.setup()
    if result.status == 'success':
        QMessageBox.information(None, "Success", "Phone emulator created and saved.")
    elif result.status == 'warning':
        if result.reason == 'proxy already taken. not recommended to use.':
            #ask user if they want to use the same proxy
            reply = QMessageBox.question(None, "Warning", "Proxy already taken. Do you want to use the same proxy?",
                                         QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                result = emulator.setup(let_same_proxy=True)
                if result.status == 'success':
                    QMessageBox.information(None, "Success", "Phone emulator created and saved.")
                else:
                    QMessageBox.critical(None, "Error", result.reason)

        else:
            QMessageBox.critical(None, "Error", result.reason)
    else:
        QMessageBox.critical(None, "Error", result.reason)
