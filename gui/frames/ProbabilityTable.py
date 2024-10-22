from .BaseTable import BaseTable
import customtkinter as ctk


class ProbabilityTable(BaseTable):
    def __init__(self, parent, rows, **kwargs):
        super().__init__(
            parent,
            title_key='probability',
            columns=2,
            rows=rows
        )
        self.headers = ["", ""]
        self.header_keys = ['attempt', 'probability']
        self.header_labels = {}

        self.set_placeholder('table_placeholder')
        self.bind_headers()

    def reset_table(self):
        self.reset()

    def bind_headers(self):
        for i, key in enumerate(self.header_keys):
            label = ctk.CTkLabel(self, text='')
            self.header_labels[key] = label
            self.localisation.bind(label, key, lambda text, index=i: self.update_header(text, index))

    def update_header(self, text, index):
        """ Update the header text at the specified index. """
        self.headers[index] = text
        self.update_table()

    def init(self):
        """ Initialize the table """
        self.data = [self.headers] + [[i, 0] for i in range(1, len(self.localisation.get_alphabet()) + 1)]
        self.update_table()

    def update_prob(self, index, new_value: int | float):
        if 1 <= index <= len(self.data) - 1:
            self.data[index][1] = new_value
            self.update_table()
