"""MenuBar Class."""

import json
from pathlib import Path
from string import Template
import darkdetect

from PyQt6.QtCore import QObject
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMenu, QMenuBar, QWidget

from letterguesser.config import DEFAULT_LANGUAGE_CODE, DEFAULT_THEME, LANGUAGES

from letterguesser.context import settings

from .ExperimentManager import ExperimentManager
from .Localisation import Localisation
from .ThemeManager import ThemeManager


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

        self.theme_manager = ThemeManager(settings, self)
        self.theme_manager.theme_changed.connect(self._update_theme_menu)
        self.theme_manager.sync_toggled.connect(self._update_theme_menu)

        self.themes_menu = QMenu("Themes", self)
        self.localisation.bind(self.themes_menu, 'themes')
        self.addMenu(self.themes_menu)
        self._populate_themes_menu()

        self.languages_menu = QMenu("Languages", self)
        self.localisation.bind(self.languages_menu, 'languages')
        self.addMenu(self.languages_menu)
        self._populate_languages_menu()

        self._load_preferences()

    def _populate_themes_menu(self) -> None:
        """Populate the themes."""
        sync_action = QAction('sync', self)
        self.localisation.bind(sync_action, 'sync')

        sync_action.setCheckable(True)
        sync_action.setData('system_sync')
        sync_action.triggered.connect(self.theme_manager.toggle_sys_sync)
        self.themes_menu.addAction(sync_action)

        for theme_folder, theme_name in self.theme_manager.theme_mapping.items():
            action = QAction(theme_name, self)
            action.setCheckable(True)
            action.setData(theme_folder)
            action.triggered.connect(
                lambda checked,
                       t=theme_folder:
                self.theme_manager.apply_theme(t)
            )
            self.themes_menu.addAction(action)

    def _populate_languages_menu(self) -> None:
        """Populate the languages menu with predefined language options."""
        for code, name in LANGUAGES.items():
            action = QAction(name, self)
            action.setCheckable(True)
            action.triggered.connect(
                lambda checked, lang=code: self.change_language(lang)
            )
            self.languages_menu.addAction(action)

    def _update_theme_menu(self, theme: str) -> None:
        """Update the themes menu to reflect the selected theme."""
        is_system_sync = self.theme_manager.is_system_sync_enabled()

        for action in self.themes_menu.actions():
            # print(f'{action.text()=}, {theme=}, {is_system_sync=}\n')
            if action.data() == 'system_sync':
                action.setChecked(is_system_sync)
            else:
                action.setChecked(
                    self.theme_manager.get_theme_name(theme) == action.text()
                )

    def _load_preferences(self) -> None:
        """
        Load user preferences from the configuration file.

        :return: Dictionary of user preferences.
        """
        theme = self.settings.value("theme", DEFAULT_THEME)
        theme_sync = self.settings.value("theme_sync", False, type=bool)

        if theme_sync:
            self.theme_manager.toggle_sys_sync()
        else:
            self.theme_manager.apply_theme(theme)

        # Apply the last saved language or default
        lang = self.settings.value("language", DEFAULT_LANGUAGE_CODE)
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
