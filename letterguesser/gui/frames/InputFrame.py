from letterguesser.gui.widgets import TextBlockSegment, InputBlock, ButtonGroup
from letterguesser.styles.padding import pad_3, pad_4, pad_5

from .BaseFrame import BaseFrame


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
                "label_key": "reset",
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

    def block_reset(self, block_name: str):
        block = self.local_blocks.get(block_name)

        if block:
            block.reset()

    def block_update_text(self, block_name: str, text: str):
        block = self.local_blocks.get(block_name)

        if block:
            block.update_value(text)

    def block_clear(self, block_name: str):
        block = self.local_blocks.get(block_name)

        if block:
            block.clear()

    def input_clear(self):
        self.input.clear()

    def input_reset(self):
        self.input.reset()

    def input_set_state(self, state):
        if state == 'disable':
            self.input.disable()
        elif state == 'enable':
            self.input.enable()
        else:
            self.input.disable()

    def update_random_text(self, text):
        self.random_text.update_value(text)

    def button_set_state(self, button_name, state):
        button = self.actions.get_button(button_name)

        if button:
            if state == 'disable':
                button.disable()
            elif state == 'enabled':
                button.enable()
            else:
                button.enable()

    def button_update_label(self, button_name, label):
        button = self.actions.get_button(button_name)

        if button and label:
            self.localisation.bind(button, label)

    def button_set_command(self, button_name, command):
        button = self.actions.get_button(button_name)

        if button and command:
            button.set_command(command)