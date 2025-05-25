from PyQt5.QtCore import QFile, QTextStream
import os
import darkdetect


class StyleLoader:
    @staticmethod
    def load_theme(theme_name: str, app):
        base_path = os.path.join(os.path.dirname(__file__), "..", "styles")

        # Определяем реальное имя темы для системного режима
        if theme_name == "system":
            system_theme = darkdetect.theme().lower()
            theme_name = system_theme if system_theme in ["dark", "light"] else "light"

        theme_file = f"{theme_name}.qss"
        file_path = os.path.join(base_path, theme_file)

        if os.path.exists(file_path):
            file = QFile(file_path)
            if file.open(QFile.ReadOnly | QFile.Text):
                stream = QTextStream(file)
                app.setStyleSheet(stream.readAll())
                file.close()