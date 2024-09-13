import sys
import time
import threading
import pywhatkit as pwk
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QWidget


class WhatsAppAutomationApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('WhatsApp Automation')

        layout = QVBoxLayout()

        # Input field for the phone number (or can be a list of numbers)
        self.phone_input = QLineEdit(self)
        self.phone_input.setPlaceholderText('Enter phone numbers separated by commas')
        layout.addWidget(QLabel('Phone Numbers:'))
        layout.addWidget(self.phone_input)

        # Input field for the message
        self.message_input = QTextEdit(self)
        self.message_input.setPlaceholderText('Enter the message to send (optional)')
        layout.addWidget(QLabel('Message:'))
        layout.addWidget(self.message_input)

        # Input field for the image path
        self.image_input = QLineEdit(self)
        self.image_input.setPlaceholderText('Enter the image file path (optional)')
        layout.addWidget(QLabel('Image Path:'))
        layout.addWidget(self.image_input)

        # Button to start automation
        self.send_button = QPushButton('Send Messages', self)
        self.send_button.clicked.connect(self.start_sending_messages)
        layout.addWidget(self.send_button)

        # Log window to show progress
        self.log_window = QTextEdit(self)
        self.log_window.setReadOnly(True)
        layout.addWidget(QLabel('Log:'))
        layout.addWidget(self.log_window)

        self.setLayout(layout)

    def log(self, text):
        """Utility function to log messages in the log window"""
        self.log_window.append(text)

    def start_sending_messages(self):
        """Start the process of sending WhatsApp messages"""
        phone_numbers = self.phone_input.text().split(',')
        message = self.message_input.toPlainText()
        image_path = self.image_input.text()

        if not phone_numbers or (not message and not image_path):
            self.log("Please provide phone numbers and either a message or an image.")
            return

        # Run pywhatkit in a separate thread to avoid blocking the GUI
        threading.Thread(target=self.send_messages, args=(phone_numbers, message, image_path)).start()

    def send_messages(self, phone_numbers, message, image_path):
        """Function to send WhatsApp messages or images"""
        try:
            for number in phone_numbers:
                number = number.strip()  # Clean up any whitespace
                if number:
                    self.log(f"Sending to {number}...")

                    if image_path:
                        # Send an image with or without a message
                        pwk.sendwhats_image(f"+{number}", image_path, caption=message or "")
                        self.log(f"Image sent to {number}")
                    elif message:
                        # Send just a text message
                        pwk.sendwhatmsg_instantly(f"+{number}", message, 15, tab_close=True, close_time=5)
                        self.log(f"Message sent to {number}")

                    time.sleep(10)  # Delay to avoid spamming and ensure smooth sending

        except Exception as e:
            self.log(f"Error: {e}")

        self.log("Process completed.")


# Main function to run the application
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WhatsAppAutomationApp()
    window.show()
    sys.exit(app.exec())
