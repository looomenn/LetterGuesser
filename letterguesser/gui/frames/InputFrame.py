"""
InputFrame for user input and control buttons.

Provides an input block, action buttons, and text displays.
"""
from typing import Optional, Callable

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame, QVBoxLayout

from letterguesser.gui.widgets import ButtonGroup, InputBlock

from letterguesser.context import localisation, manager


class InputFrame(QFrame):
    """Frame with input fields and controls for managing user input."""

    def __init__(self, **kwargs):
        """
        Initialize InputFrame with input fields and action buttons.

        :param parent: Parent tkinter object for the frame.
        """
        super().__init__(**kwargs)

        self.setObjectName('Container')

        self.manager = manager
        self.localisation = localisation

        # layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.layout.setSpacing(24)

        self.random_text = InputBlock(
            localisation_key='random_text_part',
            placeholder_key='no_input',
            is_disabled=True
        )
        self.layout.addWidget(self.random_text)

        self.used_chars = InputBlock(
            localisation_key='used_chars',
            placeholder_key='no_input',
            is_disabled=True
        )
        self.layout.addWidget(self.used_chars)

        self.input = InputBlock(
            localisation_key='main_input_label',
            placeholder_key='main_input_placeholder',
            is_disabled=True
        )
        self.layout.addWidget(self.input)

        buttons_configs = [
            {
                "type": "combobox",
                "label_key": "char_numbers",
                "command": self.manager.change_ngram,
                "values": [i for i in range(5, 55, 5)]
            },
            {
                "type": "button",
                "label_key": "reset",
                "style": "danger",
                "command": self.manager.reset_experiment,
                "is_disabled": True
            },
            {
                "type": "button",
                "label_key": "start",
                "style": "primary",
                "command": self.manager.start_experiment
            }
        ]

        self.actions = ButtonGroup(buttons_configs)
        self.layout.addWidget(self.actions)

        self.local_blocks = {
            'random_text': self.random_text,
            'used_chars': self.used_chars
        }

        self.manager.button_events['state_change'].subscribe(self.button_set_state)
        self.manager.button_events['label_change'].subscribe(self.button_update_label)
        self.manager.button_events['command_change'].subscribe(self.button_set_command)

        self.manager.input_events['state_change'].subscribe(self.input_set_state)
        self.manager.input_events['reset'].subscribe(self.input_reset)
        self.manager.input_events['clear'].subscribe(self.input_clear)

        self.manager.block_events['clear'].subscribe(self.block_clear)
        self.manager.block_events['update'].subscribe(self.block_update_text)
        self.manager.block_events['reset'].subscribe(self.block_reset)

    def block_reset(self, block_name: str) -> None:
        """Reset a specified text block."""
        block = self.local_blocks.get(block_name)

        if block:
            block.reset()

    def block_update_text(self, block_name: str, text: str) -> None:
        """Update text in a specified block."""
        block = self.local_blocks.get(block_name)

        if block:
            block.update_input(text)

    def block_clear(self, block_name: str) -> None:
        """Clear the content of a specified block."""
        block = self.local_blocks.get(block_name)

        if block:
            block.clear()

    def input_clear(self) -> None:
        """Clear the main input field."""
        self.input.clear()

    def input_reset(self) -> None:
        """Reset the main input field to default."""
        self.input.reset()

    def input_set_state(self, state: str) -> None:
        """Set the state of the input field (enable/disable)."""
        if state == 'disable':
            self.input.disable()
        elif state == 'enable':
            self.input.enable()
        else:
            self.input.disable()

    def update_random_text(self, text: str) -> None:
        """Update the random text display."""
        self.random_text.update_value(text)

    def button_set_state(self, button_name: str, state: str) -> None:
        """Set the state of a specified button."""
        button = self.actions.get_button(button_name)

        if button:
            if state == 'disable':
                button.disable()
            elif state == 'enabled':
                button.enable()
            else:
                button.enable()

    def button_update_label(self, button_name: str, label: str) -> None:
        """Update a button's label based on localization."""
        button = self.actions.get_button(button_name)

        if button and label:
            self.localisation.bind(button, label)

    def button_set_command(
            self,
            button_name: str,
            command: Optional[Callable[[str], None]]
    ) -> None:
        """Set a button's command dynamically."""
        button = self.actions.get_button(button_name)

        if button:
            button.set_command(command)
