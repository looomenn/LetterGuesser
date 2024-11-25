"""
TextBlockSegment widget for displaying text segments with localization.

This widget shows a labeled text block with localization and updates support.
"""

from typing import Any

from PyQt6.QtWidgets import QVBoxLayout, QLabel, QLineEdit, QWidget, QGridLayout
from PyQt6.QtCore import Qt

from letterguesser.styles.padding import pad_0, pad_1

from letterguesser.context import localisation, manager


class TextBlockSegment(QWidget):
    """A text block widget with localization and automatic updating."""

    def __init__(
            self,
            parent: Any,
            localisation_key: str,
            initial_text: str,
            **kwargs: Any
    ):
        """
        Initialize the TextBlockSegment with initial text and localisation.

        :param parent: The parent widget for the TextBlockSegment.
        :param localisation_key: Localisation key for the label.
        :param initial_text: Initial text to display in the text block.
        :param kwargs: Additional configuration options.
        """
        super().__init__(parent, **kwargs)

        self.localisation = localisation
        self.manager = manager

        # layout
        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(pad_0, pad_0, pad_0, pad_0)
        self.layout.setSpacing(pad_0)

        # label
        self.label = QLabel()
        self.label.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )

        # text block
        self.text_block = QLineEdit()
        self.text_block.setText(initial_text)
        self.setEnabled(False)

        self.localisation.bind(self.label, localisation_key)
        self.localisation.bind(self.text_block, 'no_input', self.update_value)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.text_block)

    def rebind(self, new_loc_key: str) -> None:
        """
        Rebind the text block to a new localization key.

        :param new_loc_key: New localization key to bind to the text block.
        """
        self.localisation.bind(self.text_block, new_loc_key, self.update_value)

    def update_value(self, new_value: str) -> None:
        """
        Update the displayed text in the text block.

        :param new_value: New text to display in the text block.
        """
        self.text_block.setText(new_value)

    def reset(self) -> None:
        """Reset the text block to the initial localization key."""
        self.localisation.bind(self.text_block, 'no_input', self.update_value)
