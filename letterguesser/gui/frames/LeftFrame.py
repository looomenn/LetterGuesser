"""
LeftFrame to display card group and user input.

This frame holds status cards, input fields, and status displays.
"""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame, QVBoxLayout

from letterguesser.gui.widgets.CardGoup import CardGroup

from letterguesser.context import localisation, manager, logger

from letterguesser.gui.frames.InputFrame import InputFrame


class LeftFrame(QFrame):
    """
    Frame containing a card group, input frame, and status frame.

    Used to display cards with experiment details, user input, and status updates.
    """

    def __init__(self, parent, **kwargs):
        """
        Initialize LeftFrame with card and input frames.

        :param parent: The parent tkinter object.
        :param kwargs: Additional keyword arguments for frame configuration.
        """
        super().__init__(parent, **kwargs)

        self.localisation = localisation
        self.manager = manager
        self.log = logger

        # layout
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        card_configs = [
            {"label_key": "experiment_number", 'initial_value': 0, 'var_type': 'int'},
            {"label_key": "attempts", 'initial_value': 0, 'var_type': 'int'},
            {"label_key": "last_char", 'initial_value': '-', 'var_type': 'str'}
        ]

        self.card_group = CardGroup(
            self,
            num_cards=len(card_configs),
            configs=card_configs
        )

        self.layout.addWidget(self.card_group)


        self.input_frame = InputFrame()
        self.layout.addWidget(self.input_frame)

        # self.status_frame = StatusFrame(self)
        # self.add_widget(
        #     self.status_frame,
        #     alignment=Qt.AlignmentFlag.AlignLeft
        # )

        self.manager.card_events['update'].subscribe(self.card_update_value)
        self.manager.card_events['reset_all'].subscribe(self.card_reset_all)
        self.manager.card_events['reset'].subscribe(self.card_reset)

    def card_reset_all(self):
        """Reset all cards."""
        self.card_group.reset_all()

    def card_update_value(self, card_name: str, value: int | str):
        """Update the specified card with a new value."""
        card = self.card_group.get_card(card_name)

        if not card:
            self.log.error(f'Invalid card "{card_name}"')
            return

        if not isinstance(value, card.get_type()):
            self.log.error(f'Invalid value type for card "{card_name}". '
                           f'Should be: {card.get_type()} ')
            return

        card.update_value(value)

    def card_reset(self, card_name: str):
        """Reset the specified card."""
        card = self.card_group.get_card(card_name)

        if not card:
            self.log.error(f'Invalid card "{card_name}"')
            return

        card.reset()
