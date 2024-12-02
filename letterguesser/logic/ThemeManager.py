"""Theme Manager."""

from PyQt6.QtCore import QObject, QSettings, pyqtSignal, QTimer
from PyQt6.QtWidgets import QApplication

from string import Template
from pathlib import Path
import darkdetect
import json

from letterguesser.logic.utils import get_resource_path, compile_scss


class ThemeManager(QObject):
    """Theme manager of the app."""

    theme_changed = pyqtSignal(str)
    sync_toggled = pyqtSignal(bool)

    def __init__(self, settings: QSettings, parent=None):
        """
        Initialize the ThemeManager.

        :param settings: QSettings instance for storing preferences.
        :param parent: Optional parent object.
        """
        super().__init__(parent)
        self.settings = settings
        self.parent = parent

        self.theme_mapping = self._load_themes()
        self.is_system_sync = self.settings.value('theme_sync', False, type=bool)
        self.current_theme = self.settings.value('theme', 'light')

        self.system_theme = darkdetect.isDark()

        self.timer = QTimer()
        self.timer.timeout.connect(self._check_system_theme)
        self.timer.start(1000)

    @staticmethod
    def _load_themes() -> dict:
        """Load available themes from the themes directory."""
        theme_mapping: dict = {}
        themes_path = get_resource_path("assets/themes")
        try:
            themes_dir = Path(themes_path)
            for theme_folder in themes_dir.iterdir():
                if theme_folder.is_dir():
                    info_file = theme_folder / "info.json"

                    if not info_file.exists():
                        continue

                    with open(info_file, 'r') as f:
                        theme_metadata = json.load(f)
                        theme_name = theme_metadata.get('name', theme_folder.stem)

                    theme_mapping[theme_folder.stem] = theme_name

            return theme_mapping

        except FileNotFoundError:
            print(f"Theme directory not found: {themes_path}")
        except Exception as e:
            print(f"Error loading themes: {e}")

    def _check_system_theme(self):
        """Check for system theme changes and update the theme if synced."""
        current_system_theme = darkdetect.isDark()
        if current_system_theme != self.system_theme:
            self.system_theme = current_system_theme
            if self.is_system_sync:
                self._apply_system_theme()

    def apply_theme(self, theme):
        """
        Apply the selected theme.

        :param theme: The name of the selected theme.
        """
        if self.is_system_sync:
            self.is_system_sync = False
            self.settings.setValue('theme_sync', False)

        themes_path = get_resource_path('assets/themes')
        theme_folder = themes_path / theme

        try:
            theme_variables = compile_scss(
                theme_folder,
                themes_path / 'primitives.scss'
            )
            base_qss_path = themes_path / 'base.qss'

            with open(base_qss_path, 'r') as base_file:
                base_template = Template(base_file.read())

            qss_content = base_template.safe_substitute(theme_variables)

            app = QApplication.instance()
            if app is not None:
                app.setStyleSheet(qss_content)

            self.settings.setValue('theme', theme)
            self.current_theme = theme

            self.theme_changed.emit(theme)

        except FileNotFoundError as e:
            print(f"Theme file (scss) not found in: {theme_folder}")
        except Exception as e:
            print(f"Error applying '{theme}': {e}")

    def _apply_system_theme(self):
        theme = 'dark' if darkdetect.isDark() else 'light'
        self.apply_theme(theme)

    def toggle_sys_sync(self):
        """Toggle system theme sync."""
        self.is_system_sync = not self.is_system_sync
        self.settings.setValue('theme_sync', self.is_system_sync)

        self.sync_toggled.emit(self.is_system_sync)

        if self.is_system_sync:
            print('toggled system theme sync')
            self._apply_system_theme()
        else:
            self.apply_theme(self.settings.value('theme', 'light'))

    def get_theme_name(self, theme_key):
        """Return the theme name."""
        return self.theme_mapping.get(theme_key, theme_key)

    def get_current_theme(self):
        """Return the current theme."""
        return self.current_theme

    def is_system_sync_enabled(self) -> bool:
        """Return whether system theme sync is enabled."""
        return self.is_system_sync
