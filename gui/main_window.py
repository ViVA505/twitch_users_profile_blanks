from PyQt5.QtWidgets import QMainWindow, QTabWidget, QStatusBar
from PyQt5.QtCore import QTimer
from gui.tabs.generate_tab import GenerateTab
from gui.tabs.settings_tab import SettingsTab
from gui.worker import WorkerThread
from gui.utils.config_manager import ConfigManager
from gui.utils.styles_loader import StyleLoader
from PyQt5.QtWidgets import QApplication
import darkdetect

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.config = ConfigManager()
        self.worker_thread = None
        self.init_ui()
        self.apply_theme()
        self.last_system_theme = None
        self.theme_check_timer = QTimer()
        self.theme_check_timer.timeout.connect(self.check_system_theme)
        self.theme_check_timer.start(5000)  # Проверка каждые 5 секунд

    def init_ui(self):
        self.setWindowTitle("Twitch Card Generator")
        self.setGeometry(100, 100, 800, 600)

        self.tab_widget = QTabWidget()
        self.generate_tab = GenerateTab(self.config)
        self.settings_tab = SettingsTab(self.config)

        self.tab_widget.addTab(self.generate_tab, "Генерация")
        self.tab_widget.addTab(self.settings_tab, "Настройки")

        self.setCentralWidget(self.tab_widget)
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.generate_tab.start_generation.connect(self.start_generation)

    def apply_theme(self):
        StyleLoader.load_theme(self.config.get_theme(), QApplication.instance())

    def start_generation(self, logins: list):
        if self.worker_thread and self.worker_thread.isRunning():
            self.status_bar.showMessage("Процесс уже запущен...")
            return

        self.worker_thread = WorkerThread(logins, self.config)
        self.worker_thread.progress_signal.connect(self.status_bar.showMessage)
        self.worker_thread.error_signal.connect(self.show_error)
        self.worker_thread.finished_signal.connect(
            lambda: self.status_bar.showMessage("Готово!"))
        self.worker_thread.start()

    def show_error(self, message):
        self.status_bar.showMessage(f"Ошибка: {message}")
        self.generate_tab.enable_ui(True)

    def check_system_theme(self):
        if self.config.get_theme() == "system":
            current_theme = darkdetect.theme().lower()
            if current_theme != self.last_system_theme:
                self.apply_theme()
                self.last_system_theme = current_theme