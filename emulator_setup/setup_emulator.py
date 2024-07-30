import os
import subprocess
import time
import logging

from androidemulator.emulator import Emulator

from GLOBAL import GLOBAL
from database import session, Phone_emulator
from proxy import Proxy, EmptyProxy



class AndroidEmulatorManager:
    def __init__(self, account_name, avd_name, proxy: Proxy | EmptyProxy):
        self.proxy = proxy
        self.account_name = account_name
        self.avd_name = avd_name
        self.emulator = Emulator(name=self.avd_name, system_image=f"system-images;android-31;default;{self.avd_name}")

        self.logger = logging.getLogger(__name__)

    def start_emulator(self):
        try:
            self.logger.info("Starting emulator...")
            self.emulator.start()
            self.logger.info("Emulator started.")
        except Exception as e:
            self.logger.error(f"Failed to start emulator: {e}")
            raise

    def set_proxy(self):
        try:
            self.logger.info("Configuring proxy...")
            proxy = Proxy.from_user_format_string(self.proxy.to_user_format_string())
            adb_command = f"adb shell settings put global http_proxy {proxy.to_selenium_wire_options()}"
            subprocess.run(adb_command.split(), check=True)
            self.logger.info("Proxy configuration successful.")
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to configure proxy: {e}")
            raise

    def save_emulator_to_database(self):
        try:
            self.logger.info("Saving emulator to database...")
            emulator = Phone_emulator(account_name=self.account_name, avd_name=self.avd_name,
                                      proxy=self.proxy.to_user_format_string())
            session.add(emulator)
            session.commit()
            self.logger.info("Emulator saved to database.")
        except Exception as e:
            self.logger.error(f"Failed to save emulator to database: {e}")
            raise

    def verify_proxy(self):
        try:
            self.logger.info("Verifying proxy configuration...")
            verify_command = "adb shell settings get global http_proxy"
            result = subprocess.run(verify_command.split(), capture_output=True, text=True, check=True)
            proxy = result.stdout.strip()
            self.logger.info(f"Proxy is set to: {proxy}")
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to verify proxy: {e}")
            raise

    def setup(self, let_same_proxy=False):
        # Check if an emulator for the given account already exists
        existing_account_emulator = session.query(Phone_emulator).filter_by(account_name=self.account_name).first()

        if existing_account_emulator:
            self.logger.info(f"Emulator for account '{self.account_name}' already exists. Skipping setup.")
            return {"status": "error", "reason": "Emulator already exists."}

        # Check if the proxy is already associated with another emulator
        proxy_as_string = self.proxy.to_user_format_string()
        existing_proxy_emulator = session.query(Phone_emulator).filter_by(proxy=proxy_as_string).first()

        if not let_same_proxy and existing_proxy_emulator:
            self.logger.info(f"Emulator for proxy '{proxy_as_string}' already exists. Skipping setup.")
            return {"status": "warning", "reason": "Proxy already taken. Not recommended to use."}

        # Start the emulator if checks pass
        self.start_emulator()

        # Ensure these steps only run if the emulator starts successfully
        # self.set_proxy()
        # self.verify_proxy()
        # self.save_emulator_to_database()

        return {"status": "success", "reason": "Emulator setup initiated."}
