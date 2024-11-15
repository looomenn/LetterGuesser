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

from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PyQt6.QtGui import QKeySequence, QShortcut

from letterguesser.config import APP_SIZE, APP_TITLE
from letterguesser.context import localisation, manager
# from letterguesser.gui.frames import HeaderFrame, MainFrame
from letterguesser.styles.padding import pad_0, pad_6


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

        #self.header_frame = HeaderFrame(self)
        #self.main_frame = MainFrame(self)

        #self.main_layout.addWidget(self.header_frame)
        #self.main_layout.addWidget(self.main_frame)

        self.init_shortcuts()

    def center(self) -> None:
        """Center the window on the screen."""
        screen_geometry = self.screen().availableGeometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)

    def init_shortcuts(self):
        """Initialize key bindings."""
        escape_shortcut = QShortcut(QKeySequence('Escape'), self)
        escape_shortcut.activated.connect(self.close)  # ignore IDE highlight

        #ctrl_l_shortcut = QShortcut(QKeySequence('Ctrl+L'), self)
        #ctrl_l_shortcut.activated.connect(self.header_frame.toggle_language)


if __name__ == "__main__":
    app = QApplication([])  # no input is planned
    windows = App()
    windows.show()
    sys.exit(app.exec())
# end main
