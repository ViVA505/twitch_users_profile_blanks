from PyQt5.QtCore import QThread, pyqtSignal
from back.TwitchAPI.handler import TwitchAPIHandler
from back.TwitchAPI.cardgenerator import TwitchCardGenerator


class WorkerThread(QThread):
    progress_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)
    finished_signal = pyqtSignal()

    def __init__(self, logins: list, config):
        super().__init__()
        self.logins = logins
        self.config = config

    def run(self):
        try:
            api_handler = TwitchAPIHandler(
                self.config.get("AUTH", "client_id"),
                self.config.get("AUTH", "client_secret")
            )

            generator = TwitchCardGenerator(
                api_handler,
                self.config.get("FONT", "path"),
                self.config.get_color()
            )

            output_dir = self.config.get("OUTPUT", "directory")

            self.progress_signal.emit("Начало генерации карточек...")
            generator.generate_all_cards(self.logins, output_dir)

            if generator.not_found_users:
                self.progress_signal.emit(
                    f"Не найдены пользователи: {', '.join(generator.not_found_users)}"
                )

            self.finished_signal.emit()

        except Exception as e:
            self.error_signal.emit(str(e))