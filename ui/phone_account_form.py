from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QMessageBox, QVBoxLayout, QComboBox

from helpers import create_and_save_phone_emulator
from proxy import Proxy, EmptyProxy
from utils.terminal import Terminal


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
                                    "and let's go\n"
                                    "3. choose system image\n"
                                    "4. choose device (use only phones in future updates we will showing only phones)\n"
                                    "5. click submit\n"
                                    "AVD it is a virtual device name can be anything\n"
                                    "but we recommend writing a name that is clear and unique\n")
        self.layout.addWidget(self.explain_label)
        # avd_name line editor
        self.avd_name_label = QLabel("Avd name:")
        self.layout.addWidget(self.avd_name_label)
        self.avd_name_input = QLineEdit()
        self.layout.addWidget(self.avd_name_input)

        self.list_available_system_images = Terminal.available_system_images()
        if len(self.list_available_system_images) == 0:
            Terminal.install_default_system_image()
            self.list_available_system_images = Terminal.available_system_images()
            if len(self.list_available_system_images) == 0:
                QMessageBox.information(self, "Error", "Could not install default system image")
        self.list_available_devices = Terminal.list_available_devices()

        # create selector
        self.comboBox_images = QComboBox()
        for image in self.list_available_system_images:
            self.comboBox_images.addItem(image.get('human_name'))
        self.layout.addWidget(self.comboBox_images)

        # create selector
        self.comboBox_devices = QComboBox()
        for device in self.list_available_devices:
            self.comboBox_devices.addItem(device)
        self.layout.addWidget(self.comboBox_devices)



        self.proxy_label = QLabel("Proxy:")
        self.layout.addWidget(self.proxy_label)
        self.proxy_input = QLineEdit()
        self.layout.addWidget(self.proxy_input)

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit)
        self.layout.addWidget(self.submit_button)

    def submit(self):
        avd_name = self.avd_name_input.text()
        image_name = self.comboBox_images.currentText()
        image = None
        for image_dict in self.list_available_system_images:
            if image_dict.get('human_name') == image_name:
                image = image_dict.get('program_name')
                break
        device = self.comboBox_devices.currentText()
        proxy = self.proxy_input.text()

        if not self.valid_proxy(proxy):
            QMessageBox.warning(self, "Invalid Proxy", "Please enter a valid proxy.")
            return
        create_and_save_phone_emulator(avd_name=avd_name, image_name=image, device_name=device, proxy=Proxy.from_user_format_string(proxy))
        self.close()

    @staticmethod
    def valid_proxy(proxy):
        # proxy validation logic here
        if proxy == "":
            return False
        test_value = Proxy.from_user_format_string(proxy)
        # if the proxy has not EmptyProxy object then save
        if not isinstance(test_value, EmptyProxy):
            return True
        else:
            return False