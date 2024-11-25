"""
Card widget for displaying a localized label with a dynamic value.

Each card has a label and a value field, supporting localization and value updates.
"""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QWidget, QGridLayout, QFrame

from letterguesser.context import localisation, manager
from letterguesser.styles.padding import pad_0, pad_2


class Card(QFrame):
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

        self.setObjectName('Card')

        self.localisation = localisation
        self.manager = manager

        self.initial_value = initial_value
        self.var_type = var_type

        # layout
        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(pad_0, pad_0, pad_0, pad_0)
        self.layout.setSpacing(pad_0)

        # value label
        self.value_label = QLabel()
        self.value_label.setObjectName('CardValueLabel')
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.update_value(initial_value)

        # description label
        self.label = QLabel()
        self.label.setObjectName('CardLabel')
        self.label.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        self.localisation.bind(self.label, loc_label_key)

        self.layout.addWidget(self.value_label)
        self.layout.addWidget(self.label)

    def update_value(self, value: str | int):
        """Update the displayed value on the card."""
        self.value_label.setText(str(value))

    def reset(self):
        """Reset the card value to the initial value."""
        self.update_value(self.initial_value)

    def get_type(self):
        """Get type of the card."""
        return str if self.var_type == "str" else int
