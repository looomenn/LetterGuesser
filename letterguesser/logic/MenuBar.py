"""MenuBar Class."""

from pathlib import Path

from PyQt6.QtCore import QObject
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMenu, QMenuBar, QWidget

from letterguesser.logic.utils import get_resource_path

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

    def _populate_themes_menu(self) -> None:
        """Populate the themes."""
        themes_path = get_resource_path("assets/themes")
        try:
            themes_dir = Path(themes_path)
            theme_files = [file.stem for file in themes_dir.glob("*.qss")]
            for theme in theme_files:
                action = QAction(theme, self)
                action.triggered.connect(lambda checked, t=theme: self._apply_theme(t))
                self.themes_menu.addAction(action)
        except FileNotFoundError:
            print(f"Theme directory not found: {themes_path}")
        except Exception as e:
            print(f"Error loading themes: {e}")

    def _populate_languages_menu(self) -> None:
        """Populate the languages menu with predefined language options."""
        english_action = QAction("English", self)
        english_action.triggered.connect(lambda: self.change_language("en"))
        self.languages_menu.addAction(english_action)

        ukrainian_action = QAction("Ukrainian", self)
        ukrainian_action.triggered.connect(lambda: self.change_language("uk"))
        self.languages_menu.addAction(ukrainian_action)

    def _apply_theme(self, theme: str) -> None:
        """
        Apply the selected theme.

        :param theme: The name of the selected theme.
        """
        theme_path = get_resource_path(f"assets/themes/{theme}.qss")
        try:
            with open(theme_path, "r") as file:
                theme_content = file.read()
                self.parent().setStyleSheet(theme_content)
        except FileNotFoundError:
            print(f"Theme file not found: {theme_path}")
        except Exception as e:
            print(f"Error applying theme: {e}")

    def change_language(self, language: str):
        """
        Change the application language based on selection.

        :param language: 'English' or 'Ukrainian'.
        """
        self.localisation.load_language(language)

        self.manager.reset_experiment()
