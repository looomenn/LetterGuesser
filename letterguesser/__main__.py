"""
LetterGuesser - Entry point.

This script allows you to run LetterGuesser as a standalone application from the
command line. Executing this module will launch CustomTkinter GUI app.

Usage:
------
To run this script, use the following command:

    python -m letterguesser

Options:
--------
No options supported
"""
import sys

from PyQt6.QtGui import QKeySequence, QShortcut
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

from letterguesser.gui.frames.LeftFrame import LeftFrame

from letterguesser.config import APP_SIZE, APP_TITLE
from letterguesser.context import localisation, manager
from letterguesser.logic.MenuBar import MenuBar
from letterguesser.styles.padding import pad_6


class App(QMainWindow):
    """Represent the main application interface."""

    def __init__(self):
        """Initialize an instance of the App class."""
        # windows setup
        super().__init__()
        self.setWindowTitle(APP_TITLE)
        self.setFixedSize(APP_SIZE[0], APP_SIZE[1])
        self.center()

        # from context set global localisation instance
        self.localisation = localisation
        self.manager = manager

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout(central_widget)
        self.main_layout.setContentsMargins(pad_6, pad_6, pad_6, pad_6)
        self.main_layout.setSpacing(pad_6)

        self.menu_bar = MenuBar(self, self.localisation, self.manager)
        self.setMenuBar(self.menu_bar)

        self.left_frame = LeftFrame(self)
        self.main_layout.addWidget(self.left_frame)

        self.init_shortcuts()

    def center(self) -> None:
        """Center the window on the screen."""
        frame_geometry = self.frameGeometry()
        screen_geometry = self.screen().availableGeometry().center()
        frame_geometry.moveCenter(screen_geometry)
        self.move(frame_geometry.topLeft())

    def init_shortcuts(self):
        """Initialize key bindings."""
        escape_shortcut = QShortcut(QKeySequence('Escape'), self)
        escape_shortcut.activated.connect(self.close)  # ignore IDE highlight


if __name__ == "__main__":
    app = QApplication([])  # no input is planned
    windows = App()
    windows.show()
    sys.exit(app.exec())
# end main
