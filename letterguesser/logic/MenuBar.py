"""MenuBar Class."""

import json
from pathlib import Path
from string import Template

from PyQt6.QtCore import QObject
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMenu, QMenuBar, QWidget

from letterguesser.config import DEFAULT_LANGUAGE_CODE, DEFAULT_THEME, LANGUAGES
from letterguesser.logic.utils import get_resource_path
from letterguesser.styles.font import fonts

from .ExperimentManager import ExperimentManager
from .Localisation import Localisation


class MenuBar(QMenuBar):
    """Menu Bar."""

    CONFIG_FILE = get_resource_path("settings.json")

    def __init__(
            self,
            parent: QObject | QWidget,
            localisation: Localisation,
            manager: ExperimentManager,
    ) -> None:
        """
        Initialize the StatusMenu.

        :param parent: Optional parent object.
        """
        super().__init__(parent)

        self.manager = manager
        self.localisation = localisation
        self.preferences = self._load_preferences()

        # themes menu
        self.themes_menu = QMenu("Themes", self)
        self.addMenu(self.themes_menu)
        self._populate_themes_menu()

        self.localisation.bind(self.themes_menu, 'themes')

        # language menu
        self.languages_menu = QMenu("Languages", self)
        self.addMenu(self.languages_menu)
        self._populate_languages_menu()

        self.localisation.bind(self.languages_menu, 'languages')

        self._apply_theme(self.preferences.get('theme', DEFAULT_THEME))
        self.change_language(self.preferences.get('language', DEFAULT_LANGUAGE_CODE))

    def _populate_themes_menu(self) -> None:
        """Populate the themes."""
        self.theme_mapping: dict = {}
        themes_path = get_resource_path("assets/themes")
        try:
            themes_dir = Path(themes_path)

            for theme_folder in themes_dir.iterdir():
                if theme_folder.is_dir():
                    info_file = theme_folder / "info.json"
                    theme_file = theme_folder / "theme.qss"

                    if not info_file.exists() or not theme_file.exists():
                        continue

                    with open(info_file, 'r') as f:
                        theme_metadata = json.load(f)
                        theme_name = theme_metadata.get('name', theme_folder.stem)

                    self.theme_mapping[theme_folder.stem] = theme_name

                    action = QAction(theme_name, self)
                    action.setCheckable(True)
                    action.triggered.connect(
                        lambda checked, t=theme_folder.stem: self._apply_theme(t)
                    )
                    self.themes_menu.addAction(action)

        except FileNotFoundError:
            print(f"Theme directory not found: {themes_path}")
        except Exception as e:
            print(f"Error loading themes: {e}")

    def _populate_languages_menu(self) -> None:
        """Populate the languages menu with predefined language options."""
        languages = {
            "en": "English",
            "uk": "Ukrainian"
        }

        for code, name in languages.items():
            action = QAction(name, self)
            action.setCheckable(True)
            action.triggered.connect(
                lambda checked, lang=code: self.change_language(lang)
            )
            self.languages_menu.addAction(action)

    def _apply_theme(self, theme: str) -> None:
        """
        Apply the selected theme.

        :param theme: The name of the selected theme.
        """
        theme_path = get_resource_path(f"assets/themes/{theme}/theme.qss")
        try:
            with open(theme_path, "r") as file:
                qss_template = Template(file.read())

            qss_content = qss_template.safe_substitute(fonts)

            self.parent().setStyleSheet(qss_content)

            self.preferences["theme"] = theme
            self._save_preferences()

            for action in self.themes_menu.actions():
                action.setChecked(
                    self.theme_mapping.get(theme) == action.text()
                )

        except FileNotFoundError:
            print(f"Theme file not found: {theme_path}")
        except Exception as e:
            print(f"Error applying theme: {e}")

    def _load_preferences(self) -> dict:
        """
        Load user preferences from the configuration file.

        :return: Dictionary of user preferences.
        """
        try:
            with open(self.CONFIG_FILE, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _save_preferences(self) -> None:
        """Save user preferences to the configuration file."""
        try:
            with open(self.CONFIG_FILE, "w") as file:
                json.dump(self.preferences, file, indent=4)
        except Exception as e:
            print(f"Error saving preferences: {e}")

    def change_language(self, language: str):
        """
        Change the application language based on selection.

        :param language: 'English' or 'Ukrainian'.
        """
        self.localisation.load_language(language)

        self.manager.reset_experiment()

        self.preferences['language'] = language

        self._save_preferences()

        for action in self.languages_menu.actions():
            action.setChecked(action.text() == LANGUAGES.get(language))
