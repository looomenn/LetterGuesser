"""
Button widget with customizable styles and localization support.

This widget provides a styled button with various configurations (e.g., default,
primary, danger) and supports localization for its label.
"""

from typing import Callable, Optional

from PyQt6.QtCore import Qt, QVariantAnimation
from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import QPushButton

from letterguesser.context import localisation


class Button(QPushButton):
    """A customizable button with styles, localization, and enable/disable states."""

    def __init__(
            self,
            label: str,
            style: str = 'default',
            command: Optional[Callable[[str], None]] = None,
            is_disabled: bool = False,
            **kwargs
    ):
        """
        Initialise Button widget.

        :param label: Localisation key for the button label.
        :param style: Variant of the button (primary, secondary, danger)
        :param command: Function to assign with button (when clicking)
        :param is_disabled: Whether the button starts disabled, by default False.
        :param kwargs: Additional keyword arguments.
        """
        super().__init__(**kwargs)

        self.localisation = localisation
        self.style = style
        self.is_disabled = is_disabled
        self.label = label

        self.localisation.bind(self, label)

        if command:
            self.clicked.connect(command)

        self.apply_style()

        if self.is_disabled:
            self.disable()

        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

    def reset(self):
        """Reset the button."""
        self.localisation.bind(self, self.label)

    def set_command(self, command: Callable[[], None]):
        """Set specified command for the button."""
        self.clicked.disconnect()
        self.clicked.connect(command)

    def apply_style(self):
        """Apply style based on the button's state and style."""
        self.setProperty('class', f'btn-{self.style}')

    def enable(self):
        """Enable the button, making it clickable."""
        self.setDisabled(False)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

    def disable(self):
        """Disable the button, preventing interaction."""
        self.setCursor(QCursor(Qt.CursorShape.WaitCursor))
        self.setDisabled(True)
