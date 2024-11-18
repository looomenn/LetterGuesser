"""
Card widget for displaying a localized label with a dynamic value.

Each card has a label and a value field, supporting localization and value updates.
"""

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLabel, QWidget

from letterguesser.gui.frames.BaseFrame import BaseFrame
from letterguesser.styles.font import (
    font,
    text_medium,
    text_small,
)
from letterguesser.styles.padding import pad_0, pad_2, pad_3


class Card(BaseFrame):
    """Displays a label and a dynamic value."""

    def __init__(
            self,
            parent: QWidget,
            loc_label_key: str,
            initial_value: str | int,
            var_type: str = 'str',
            **kwargs
    ):
        """
        Init a Card.

        :param parent: The parent widget.
        :param loc_label_key: The key of the localization label
        :param initial_value: Initial value of the card
        :param var_type: The type of variable
        :param kwargs: Additional keyword arguments
        """
        super().__init__(parent, **kwargs)

        self.initial_value = initial_value
        self.var_type = var_type

        # layout
        self.layout.setContentsMargins(pad_3, pad_3, pad_3, pad_3)
        self.layout.setSpacing(pad_2)

        # value label
        self.value_label = QLabel(self)
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.value_label.setFont(QFont(
            font, text_medium, QFont.Weight.DemiBold
        ))
        self.update_value(initial_value)

        self.add_widget(
            widget=self.value_label,
            alignment=Qt.AlignmentFlag.AlignLeft,
            margin=(pad_3, pad_3, pad_3, pad_3)
        )

        # description label
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.value_label.setFont(QFont(font, text_small))

        # bind localisation
        self.localisation.bind(self.label, loc_label_key)

        self.add_widget(
            widget=self.label,
            alignment=Qt.AlignmentFlag.AlignLeft,
            margin=(pad_3, pad_2, pad_3, pad_0)
        )

    def update_value(self, value: str | int):
        """Update the displayed value on the card."""
        self.value_label.setText(str(value))

    def reset(self):
        """Reset the card value to the initial value."""
        self.update_value(self.initial_value)

    def get_type(self):
        """Get type of the card."""
        return str if self.var_type == "str" else int
