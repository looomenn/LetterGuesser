from letterguesser.gui.widgets.CardGoup import CardGroup
from letterguesser.styles.padding import pad_0, pad_2\

from .BaseFrame import BaseFrame
from .InputFrame import InputFrame
from .StatusFrame import StatusFrame


class LeftFrame(BaseFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, transparent_bg=True, **kwargs)

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

        self.manager.card_events['update'].subscribe(self.card_update_value)
        self.manager.card_events['reset_all'].subscribe(self.card_reset_all)
        self.manager.card_events['reset'].subscribe(self.card_reset)

    def card_reset_all(self):
        self.card_group.reset_all()

    def card_update_value(self, card_name, value):
        card = self.card_group.get_card(card_name)

        if not card:
            self.log.error(f'Invalid card "{card_name}"')
            return

        if not isinstance(value, card.get_type()):
            self.log.error(f'Invalid value type for card "{card_name}". Should be: {card.get_type()} ')
            return

        card.update_value(value)

    def card_reset(self, card_name):
        card = self.card_group.get_card(card_name)

        if not card:
            self.log.error(f'Invalid card "{card_name}"')
            return

        card.reset()
