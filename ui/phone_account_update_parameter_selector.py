from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QComboBox, QLabel, QMessageBox, QInputDialog

from database import Phone_emulator, session
from proxy import Proxy
from utils.terminal import Terminal


class PhoneAccountUpdateParameterSelector(QWidget):

    def __init__(self, phone_emulator: str):
        super().__init__()
        self.phone_emulator = phone_emulator
        self.phone_emulator_object = session.query(Phone_emulator).filter(
            Phone_emulator.avd_name == phone_emulator).first()
        self.layout = QVBoxLayout()
        self.label = QLabel("Select Parameter to Update:")
        self.parameter_selector = QComboBox()
        self.update_button = QPushButton("Update")
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Update Parameters")
        self.resize(300, 200)

        self.setLayout(self.layout)

        self.layout.addWidget(self.label)

        self.parameter_selector.addItems(["Proxy", "AVD and Account Name"])
        self.layout.addWidget(self.parameter_selector)

        self.update_button.clicked.connect(self.update_parameter)
        self.layout.addWidget(self.update_button)

    def update_parameter(self):
        selected_parameter = self.parameter_selector.currentText()

        if selected_parameter == "Proxy":

            new_value, ok = QInputDialog.getText(
                self, "Update Proxy", "Enter new proxy:")

            if ok:
                try:
                    proxy = new_value
                except ValueError as e:
                    QMessageBox.warning(self, "Invalid input", str(e))
                    return
                if not Proxy.from_user_format_string(proxy):
                    QMessageBox.warning(self, "Invalid input",
                                        "Please enter a valid proxy.")
                    return
                session.commit()
                self.phone_emulator_object.proxy = proxy
                Terminal.update_parameters(
                    self.phone_emulator_object.avd_name,
                    self.phone_emulator_object.account_name,
                    Proxy.from_user_format_string(proxy))
        elif selected_parameter == "AVD and Account Name":
            new_value, ok = QInputDialog.getText(
                self, "Update AVD and Account Name",
                "Enter new AVD and Account Name (no spaces, only '_'):")
            if ok:
                if not all(
                        char.isalnum() or char == "_"
                        for char in new_value
                ):
                    QMessageBox.warning(
                        self, "Invalid input",
                        "AVD and Account Name can contain only "
                        "letters, numbers and '_'.")
                    return
                avd_name = "SDE_"+new_value
                account_name = "SDE_"+new_value
                self.phone_emulator_object.avd_name = avd_name
                self.phone_emulator_object.account_name = account_name
                session.commit()
                Terminal.update_parameters(
                    avd_name, account_name,
                    Proxy.from_user_format_string(
                        self.phone_emulator_object.proxy))
