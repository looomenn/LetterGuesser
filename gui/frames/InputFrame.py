# frames
from .BaseFrame import BaseFrame

# widgets
from gui.widgets import *

# utils
from styles.padding import *


class InputFrame(BaseFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.random_text = TextBlockSegment(
            self,
            localisation_key='random_text_part',
            initial_text='-'
        )
        self.add_widget(
            self.random_text,
            side='top',
            expand=False,
            padx=pad_5,
            pady=(pad_5, pad_3)
        )

        self.used_chars = TextBlockSegment(
            self,
            localisation_key='used_chars',
            initial_text='-'
        )
        self.add_widget(
            self.used_chars,
            side='top',
            expand=False,
            padx=pad_5,
            pady=(pad_3, pad_4)
        )

        self.input = InputBlock(
            self,
            loc_label_key='main_input_label',
            loc_placeholder_key='main_input_placeholder',
            is_disabled=True
        )
        self.add_widget(
            self.input,
            side='top',
            expand=False,
            padx=pad_5,
            pady=pad_4
        )

        buttons_configs = [
            {
                "type": "option_menu",
                "label_key": "char_numbers",
                "initial_value": 5,
                "command": self.manager.change_ngram,
                "values": [i for i in range(5, 55, 5)]
            },
            {
                "type": "button",
                "label_key": "reset_button_label",
                "style": "danger",
                "command": self.manager.reset_experiment,
                "is_disabled": True
            },
            {
                "type": "button",
                "label_key": "start",
                "style": "primary",
                "command": self.manager.start_experiment,
            }
        ]

        self.actions = ButtonGroup(self, buttons_configs)
        self.add_widget(
            self.actions,
            side='top',
            expand=False,
            pady=(pad_4, pad_5),
            padx=pad_5
        )

        self.manager.load_widgets({
            "random_text": self.random_text,
            "used_chars": self.used_chars,
            "input": self.input,
            "actions": self.actions
        })
