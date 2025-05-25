from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QFileDialog, QGroupBox, QComboBox)
from PyQt5.QtCore import Qt
from pathlib import Path
from gui.widgets.color_button import ColorButton
from gui.utils.styles_loader import StyleLoader
from PyQt5.QtWidgets import QApplication
from typing import Tuple
import darkdetect


class SettingsTab(QWidget):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.init_ui()
        self.setup_theme_selector()
        self.load_config_values()
        self.color_btn.color_changed.connect(self.save_color)


    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Auth Group
        auth_group = QGroupBox("Настройки Twitch API")
        auth_layout = QVBoxLayout()

        # Client ID
        client_id_layout = QHBoxLayout()
        client_id_layout.addWidget(QLabel("Client ID:"))
        self.client_id_input = QLineEdit()
        client_id_layout.addWidget(self.client_id_input)
        auth_layout.addLayout(client_id_layout)

        # Client Secret
        client_secret_layout = QHBoxLayout()
        client_secret_layout.addWidget(QLabel("Client Secret:"))
        self.client_secret_input = QLineEdit()
        self.client_secret_input.setEchoMode(QLineEdit.Password)
        client_secret_layout.addWidget(self.client_secret_input)
        auth_layout.addLayout(client_secret_layout)

        auth_group.setLayout(auth_layout)
        main_layout.addWidget(auth_group)

        # Appearance Group
        appearance_group = QGroupBox("Внешний вид")
        appearance_layout = QVBoxLayout()

        # Theme Selector
        theme_layout = QHBoxLayout()
        theme_layout.addWidget(QLabel("Тема интерфейса:"))
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Системная", "Светлая", "Тёмная"])
        theme_layout.addWidget(self.theme_combo)
        appearance_layout.addLayout(theme_layout)

        # Text Color
        color_layout = QHBoxLayout()
        color_layout.addWidget(QLabel("Цвет текста:"))
        self.color_btn = ColorButton()
        color_layout.addWidget(self.color_btn)
        appearance_layout.addLayout(color_layout)

        # Font Selector
        font_layout = QHBoxLayout()
        self.font_btn = QPushButton("Выбрать шрифт")
        self.font_btn.clicked.connect(self.select_font)
        self.font_label = QLabel("Шрифт не выбран")
        font_layout.addWidget(self.font_btn)
        font_layout.addWidget(self.font_label)
        appearance_layout.addLayout(font_layout)

        # Output Directory
        output_layout = QHBoxLayout()
        self.output_btn = QPushButton("Папка сохранения")
        self.output_btn.clicked.connect(self.select_output_dir)
        self.output_label = QLabel("Папка не выбрана")
        output_layout.addWidget(self.output_btn)
        output_layout.addWidget(self.output_label)
        appearance_layout.addLayout(output_layout)

        appearance_group.setLayout(appearance_layout)
        main_layout.addWidget(appearance_group)

        # Save Button
        self.save_btn = QPushButton("Сохранить настройки")
        self.save_btn.clicked.connect(self.save_settings)
        main_layout.addWidget(self.save_btn)

        self.setLayout(main_layout)

    def setup_theme_selector(self):
        theme_mapping = {"system": 0, "light": 1, "dark": 2}
        current_theme = self.config.get_theme()

        # Для системной темы показываем актуальное состояние
        if current_theme == "system":
            system_theme = darkdetect.theme().lower()
            self.theme_combo.setCurrentIndex(theme_mapping.get(system_theme, 0))
        else:
            self.theme_combo.setCurrentIndex(theme_mapping.get(current_theme, 0))

        self.theme_combo.currentIndexChanged.connect(self.change_theme)

    def change_theme(self, index):
        themes = ["system", "light", "dark"]
        self.config.set_theme(themes[index])
        StyleLoader.load_theme(themes[index], QApplication.instance())

    def select_font(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Выберите файл шрифта", "", "Font Files (*.ttf *.otf)")
        if path:
            self.font_label.setText(Path(path).name)
            self.config.set("FONT", "path", path)

    def select_output_dir(self):
        path = QFileDialog.getExistingDirectory(self, "Выберите папку для сохранения")
        if path:
            self.output_label.setText(path)
            self.config.set("OUTPUT", "directory", path)

    def save_settings(self):
        self.config.set("AUTH", "client_id", self.client_id_input.text())
        self.config.set("AUTH", "client_secret", self.client_secret_input.text())
        self.config.save()

    def load_config_values(self):
        self.client_id_input.setText(self.config.get("AUTH", "client_id"))
        self.client_secret_input.setText(self.config.get("AUTH", "client_secret"))
        self.font_label.setText(Path(self.config.get("FONT", "path")).name)
        self.output_label.setText(self.config.get("OUTPUT", "directory"))
        self.color_btn.set_color(self.config.get_color())

    def save_color(self, color: Tuple[int, int, int, int]):
        """Сразу сохраняем цвет при изменении"""
        self.config.set_color(color)