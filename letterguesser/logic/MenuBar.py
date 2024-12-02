"""MenuBar Class."""

import json
from pathlib import Path
from string import Template

from PyQt6.QtCore import QObject, QSettings
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMenu, QMenuBar, QWidget

from letterguesser.config import DEFAULT_LANGUAGE_CODE, DEFAULT_THEME, LANGUAGES
from letterguesser.logic.utils import get_resource_path, compile_scss

from letterguesser.context import settings

from .ExperimentManager import ExperimentManager
from .Localisation import Localisation


class MenuBar(QMenuBar):
    """Menu Bar."""

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
        self.settings = settings

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
        self._load_preferences()


    def _populate_themes_menu(self) -> None:
        """Populate the themes."""
        self.theme_mapping: dict = {}
        themes_path = get_resource_path("assets/themes")
        try:
            themes_dir = Path(themes_path)

            for theme_folder in themes_dir.iterdir():
                if theme_folder.is_dir():
                    info_file = theme_folder / "info.json"
                    theme_file = theme_folder / "theme.scss"

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
        self.settings.setValue('theme', theme)
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

            self.parent().setStyleSheet(qss_content)

            for action in self.themes_menu.actions():
                action.setChecked(
                    self.theme_mapping.get(theme) == action.text()
                )

        except FileNotFoundError as e:
            print(f"Theme file (scss) not found in: {theme_folder}")
        except Exception as e:
            print(f"Error applying '{theme}': {e}")

    def _load_preferences(self) -> None:
        """
        Load user preferences from the configuration file.

        :return: Dictionary of user preferences.
        """
        theme = self.settings.value('theme', DEFAULT_THEME)
        self._apply_theme(theme)

        lang = self.settings.value('language', DEFAULT_LANGUAGE_CODE)
        self.change_language(lang)

    def change_language(self, language: str):
        """
        Change the application language based on selection.

        :param language: 'English' or 'Ukrainian'.
        """
        self.settings.setValue('language', language)

        self.localisation.load_language(language)
        self.manager.reset_experiment()

        for action in self.languages_menu.actions():
            action.setChecked(action.text() == LANGUAGES.get(language))
