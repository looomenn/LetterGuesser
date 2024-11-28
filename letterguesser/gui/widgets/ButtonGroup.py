"""
ButtonGroup widget to manage a collection of buttons and option menus.

This class allows organizing multiple buttons with shared settings and access.
"""

from typing import Any, Dict, Union


from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame, QHBoxLayout

from .Button import Button
from .ComboBox import ComboBox


def to_bool(value: str | bool) -> bool:
    """Convert string to bool."""
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() in ("yes", "true", "t", "1")


def to_list(value: str | list[str]) -> list[str]:
    """Ensure the value is a list."""
    if isinstance(value, list):
        return [str(item) for item in value]
    elif isinstance(value, str):
        return [value]


def _create_button(config: Dict[str, Any]) -> Button:
    """Create a `Button` based on the configuration."""
    is_disabled = to_bool(config.get('is_disabled', False))
    command = config.get('command', None)

    return Button(
        label=config['label_key'],
        style=config.get('style', 'default'),
        command=command,
        is_disabled=is_disabled
    )


def _create_combobox(config: Dict[str, Any]) -> ComboBox:
    """Create a `ComboBox` based on the configuration"""
    values = to_list(config.get('values', []))
    command = config.get('command', None)

    return ComboBox(
        label=config['label_key'],
        values=values,
        command=command
    )


class ButtonGroup(QFrame):
    """A container for managing buttons and option menus."""

    def __init__(
            self,
            configs: list[dict[str, Any]],
            gap: int = 10,
            **kwargs: Any
    ):
        """
        Init ButtonGroup class.

        :param configs: List of button configurations (label_key, style, etc.).
        :param gap: The gap between buttons, by default pad_2.
        :param kwargs: Additional keywords for CTkButton class
        """
        super().__init__(**kwargs)

        self.setObjectName('btn-group')

        self.layout = QHBoxLayout(self)
        self.layout.setSpacing(gap)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.buttons: Dict[str, Union[Button, ComboBox]] = {}

        for i, config in enumerate(configs):

            widget_type = config.get('type', 'button')

            if widget_type == 'button':
                item = _create_button(config)
            elif widget_type == 'combobox':
                item = _create_combobox(config)
            else:
                raise ValueError(f"Unsupported widget type: {widget_type}")

            self.layout.addWidget(item)
            self.buttons[f'button_{config["label_key"]}'] = item

    def get_button(self, key: str) -> Button | None:
        """
        Return a specific button by its `key` if available.

        :param key: The key of the button (e.g., 'button_<label_key>')
        :return: The Button instance or None if not found.
        """
        return self.buttons.get(key, None)

    def disable(self, key: str) -> None:
        """
        Disable the button identified by `key`.

        :param key: The identifier of the button to disable.
        :return: None
        """
        button = self.get_button(key)
        if button:
            button.disable()

    def enable(self, key: str) -> None:
        """
        Enable the button identified by `key`.

        :param key: The identifier of the button to enable.
        :return: None
        """
        button = self.get_button(key)
        if button:
            button.enable()

    def update_label(self, key: str, new_label_key: str) -> None:
        """
        Update the label of a button based on localisation key.

        :param key: Identifier for the target button.
        :param new_label_key: Localisation key for the new label text.
        :return: None
        """
        button = self.get_button(key)
        if button:
            button.localisation.bind(button, new_label_key)

    def enable_all(self) -> None:
        """Enable all buttons in the group."""
        for button in self.buttons.values():
            button.enable()

    def disable_all(self) -> None:
        """Disable all buttons in the group."""
        for button in self.buttons.values():
            button.disable()
