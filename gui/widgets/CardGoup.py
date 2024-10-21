""" Gives ability to create card groups """

from gui.frames.BaseFrame import BaseFrame
from .Card import Card

from styles.padding import *


class CardGroup(BaseFrame):
    def __init__(self,
                 parent,
                 num_cards,
                 configs,
                 **kwargs
                 ):
        """
        Initialize the CardGroup
        :param parent: The parent widget.
        :param num_cards: Number of cards to create.
        :param configs: A list of dictionaries containing:
                    {
                        'label_key': str (localisation key for card label)
                        'initial_value' str/int (initial value for the card).
                        'var_type': 'str' or 'int' (type of value to store)
                    }.
        :param kwargs: Additional keyword arguments.
        """
        super().__init__(parent, transparent_bg=True, **kwargs)

        self.cards = {}

        for i in range(num_cards):
            config = configs[i]
            card = Card(
                self,
                loc_label_key=config['label_key'],
                initial_value=config['initial_value'],
                var_type=config.get('var_type', 'str')
            )

            # adding the card to the layout
            self.add_widget(
                card,
                side='left',
                fill='x',
                expand=True,
                padx=(pad_0, pad_4) if i < num_cards - 1 else pad_0
            )

            # storing the card instance in the dict
            self.cards[f'card_{config["label_key"]}'] = card

    def get_card(self, key) -> Card | None:
        """
        Returns a specific card by its key.
        :param key: The key of the card (e.g., 'card_<label_key>')
        :return: The Card instance or None if not found.
        """
        return self.cards.get(key, None)

    def update_card_value(self, key: str, value: str | int) -> None:
        """
        Updates the value of a specific card.
        :param key: The key of the card (e.g., 'card_<label_key>').
        :param value: The new value to set in the card.
        :return: None
        """
        card = self.get_card(key)
        if card:
            card.update_value(value)

    def reset(self, key: str) -> None:
        """
        Resets the value of a specific card.
        :param key: The key of the card (e.g., 'card_<label_key>')
        :return: None
        """

        card = self.get_card(key)
        if card:
            card.reset()
