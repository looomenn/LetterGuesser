# frames
from .BaseFrame import BaseFrame
from .InputFrame import InputFrame
from .StatusFrame import StatusFrame

# widgets
from gui.widgets.CardGoup import CardGroup

# utils
from styles.padding import *


class LeftFrame(BaseFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, transparent_bg=True, **kwargs)

        card_configs = [
            {"label_key": "experiment_number", 'initial_value': 0, 'var_type': 'int'},
            {"label_key": "attempts", 'initial_value': '-', 'var_type': 'str'},
            {"label_key": "last_char", 'initial_value': '-', 'var_type': 'str'}
        ]

        self.card_group = CardGroup(
            self,
            num_cards=len(card_configs),
            configs=card_configs
        )

        self.add_widget(
            self.card_group,
            side='top',
            expand=False,
            pady=(pad_0, pad_2)
        )

        self.input_frame = InputFrame(self)
        self.add_widget(self.input_frame, side='top', expand=False, pady=pad_2)

        self.status_frame = StatusFrame(self)
        self.add_widget(self.status_frame, side='top', fill='both', expand=True, pady=(pad_2, pad_0))
