from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPlainTextEdit, QPushButton, QMessageBox
from PyQt5.QtCore import pyqtSignal


class GenerateTab(QWidget):
    start_generation = pyqtSignal(list)

    def __init__(self, config):
        super().__init__()
        self.config = config
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.input_field = QPlainTextEdit()
        self.input_field.setPlaceholderText("Введите логины (каждый с новой строки)...")

        self.generate_btn = QPushButton("Сгенерировать карточки")
        self.generate_btn.clicked.connect(self.validate_and_start)

        layout.addWidget(self.input_field)
        layout.addWidget(self.generate_btn)
        self.setLayout(layout)

    def validate_and_start(self):
        logins = [login.strip() for login in self.input_field.toPlainText().splitlines() if login.strip()]

        if not logins:
            QMessageBox.warning(self, "Ошибка", "Введите хотя бы один логин")
            return

        if not self.config.validate_credentials():
            QMessageBox.critical(self, "Ошибка", "Необходимо указать Client ID и Client Secret в настройках!")
            return

        self.start_generation.emit(logins)

    def enable_ui(self, enabled: bool):
        self.input_field.setEnabled(enabled)
        self.generate_btn.setEnabled(enabled)