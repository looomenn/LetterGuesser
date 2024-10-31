from .BaseScrollFrame import BaseScrollFrame

from letterguesser.gui.widgets.List import List
from letterguesser.styles.padding import pad_2, pad_3


class AttemptsList(BaseScrollFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            title_key='guessed_chars',
            **kwargs
        )

        self.list = List(self)

        self.set_placeholder('table_placeholder')
        self.update_list()

    def update_list(self):
        data = self.list.get_items()

        if not data:
            self.show_placeholder()
            self.list.pack_forget()
        else:
            self.hide_placeholder()
            self.list.pack(side='top', fill='both', expand=True, padx=pad_3, pady=(pad_2, pad_3))

    def add_char(self, char, attempt):
        alphabet_len = len(self.localisation.get_alphabet())

        binary = ['0'] * alphabet_len
        if attempt <= alphabet_len:
            binary[attempt - 1] = '1'

        binary_string = ''.join(binary)
        res = {
            'leading': {'key': 'attempt', 'value': attempt},
            'trailing': {'key': 'char', 'value': char},
            'sub': {'key': None, 'value': binary_string}
        }

        self.list.add_item(res)
        self.update_list()

    def reset(self):
        self.list.clear()
        self.update_list()
