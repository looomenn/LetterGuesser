"""
OptionMenu widget for a dropdown menu with localization and hover effects.

This widget provides an option menu that supports localization and changes appearance
on hover.
"""

from typing import Any, Callable, Optional

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import QComboBox

from letterguesser.context import localisation


class ComboBox(QComboBox):
    """A dropdown menu with localization, hover effects, and enable/disable states."""

    def __init__(
            self,
            label: str,
            values: list[str],
            command: Optional[Callable[[str], None]] = None,
            **kwargs: Any
    ) -> None:
        """
        Initialize the OptionMenu with values and localization key.

        :param parent: Parent tkinter widget/frame for the OptionMenu.
        :param label_key: Localization key for the menu label.
        :param values: List of options available in the menu.
        :param command: Command to execute on selection change.
        :param kwargs: Additional configuration options.
        """
        super().__init__(**kwargs)

        self.values = values
        self.label = label
        self.localisation = localisation
        self.command = command

        self.addItems(values)

        if values:
            self.setCurrentText(values[0])

        self.localisation.bind(self, label, self.update_loc)

        self.currentTextChanged.connect(self.on_selection_changed)

        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

    def on_selection_changed(self, value: str) -> None:
        """
        Handle the selection change event.

        :param value: The selected value.
        """
        if self.command:
            self.command(value)

    def disable(self) -> None:
        """Disable the OptionMenu, preventing user interaction."""
        self.setEnabled(False)
        self.setCursor(QCursor(Qt.CursorShape.ForbiddenCursor))

    def enable(self) -> None:
        """Enable the OptionMenu, allowing user interaction."""
        self.setEnabled(True)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

    def update_loc(self, text) -> None:
        """
        Update localized text for the OptionMenu items.

        :param text: Localized suffix text for each menu item.
        :return: None
        """
        current_index = self.currentIndex()
        formatted_values = [f"{val} {text}" for val in self.values]

        self.clear()
        self.addItems(formatted_values)
        self.setCurrentIndex(current_index)
