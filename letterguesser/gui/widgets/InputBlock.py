"""
InputBlock widget with a label and entry field.

This block provides an input field with a localized label and optional placeholder.
"""

from typing import Any

from PyQt6.QtWidgets import QVBoxLayout, QLabel, QLineEdit, QWidget
from PyQt6.QtCore import Qt

from letterguesser.context import localisation, manager


class InputBlock(QWidget):
    """Input block with a label and entry field."""

    def __init__(
            self,
            localisation_key,
            placeholder_key: str | None = None,
            initial_text: str = '-',
            is_disabled=False,
            **kwargs: Any
    ):
        """
        Init InputBlock.

        :param localisation_key: Localization key for the label.
        :param placeholder_key: Localization key for the placeholder text.
        :param initial_text: Initial text to display in the input field.
        :param is_disabled: Whether the input block should be disabled initially.
        :param kwargs: Additional configuration options.
        """
        super().__init__(**kwargs)

        self.setObjectName('form-group')

        self.localisation = localisation
        self.manager = manager
        self.placeholder_key = placeholder_key

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(6)

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.localisation.bind(self.label, localisation_key)
        self.layout.addWidget(self.label)

        self.input_field = QLineEdit()

        self.layout.addWidget(self.input_field)

        if placeholder_key:
            self.localisation.bind(self.input_field, placeholder_key, self.update_input)
        else:
            self.input_field.setText(initial_text)

        if is_disabled:
            self.disable()

        self.input_field.returnPressed.connect(self.input_handler)

    def reset(self):
        """Reset the input block to its default state with the placeholder."""
        self.localisation.bind(
            self.input_field,
            self.placeholder_key,
            self.update_input
        )

    def input_handler(self) -> None:
        """Handle input events and forward the input to the manager."""
        self.manager.input_handler(self.get_input())

    def get_input(self) -> Any:
        """Return the current input value."""
        return self.input_field.text()

    def clear(self) -> None:
        """Clear the input field content."""
        self.input_field.clear()

    def update_input(self, new_value: str) -> None:
        """
        Update the input field with a new value.

        :param new_value: The value to set in the input field.
        :return: None
        """
        self.input_field.setText(new_value)

    def enable(self):
        """Enable the input field for user entry."""
        self.input_field.setEnabled(True)

    def disable(self):
        """Disable the input field to prevent interaction."""
        self.input_field.setEnabled(False)

    def rebind(self, localisation_key: str) -> None:
        """
        Rebind the text block to a new localization key.

        :param localisation_key: New localization key to bind to the text block.
        """
        self.localisation.bind(self.input_field, localisation_key, self.update_input)