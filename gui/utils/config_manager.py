import configparser
from typing import Tuple
from pathlib import Path

class ConfigManager:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config_file = Path("config.ini")
        self.defaults = {
            "AUTH": {"client_id": "", "client_secret": ""},
            "FONT": {"path": ""},
            "COLOR": {"r": "255", "g": "215", "b": "0", "a": "255"},
            "OUTPUT": {"directory": "output"},
            "THEME": {"name": "system"}
        }
        self.ensure_config()

    def ensure_config(self):
        if not self.config_file.exists():
            self.create_default_config()
        else:
            self.config.read(self.config_file)
            self.add_missing_sections()

    def create_default_config(self):
        for section, options in self.defaults.items():
            self.config[section] = options
        self.save()

    def add_missing_sections(self):
        for section, options in self.defaults.items():
            if not self.config.has_section(section):
                self.config.add_section(section)
            for key, value in options.items():
                if not self.config.has_option(section, key):
                    self.config.set(section, key, value)
        self.save()

    def validate_credentials(self) -> bool:
        return bool(self.get("AUTH", "client_id")) and bool(self.get("AUTH", "client_secret"))

    def get(self, section: str, key: str) -> str:
        return self.config.get(section, key, fallback=self.defaults.get(section, {}).get(key, ""))

    def set(self, section: str, key: str, value: str):
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, key, value)
        self.save()

    def save(self):
        with open(self.config_file, "w") as f:
            self.config.write(f)

    def get_color(self) -> Tuple[int, int, int, int]:
        color = (
            int(self.get("COLOR", "r")),
            int(self.get("COLOR", "g")),
            int(self.get("COLOR", "b")),
            int(self.get("COLOR", "a"))
        )
        print(f"Loading color: {color}")  # Для отладки
        return color

    def set_color(self, color: Tuple[int, int, int, int]):
        print(f"Saving color: {color}")  # Для отладки
        self.set("COLOR", "r", str(color[0]))
        self.set("COLOR", "g", str(color[1]))
        self.set("COLOR", "b", str(color[2]))
        self.set("COLOR", "a", str(color[3]))
        self.save()

    def get_theme(self) -> str:
        return self.get("THEME", "name")

    def set_theme(self, theme_name: str):
        self.set("THEME", "name", theme_name)