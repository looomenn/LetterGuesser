from .BaseTable import BaseTable
import customtkinter as ctk


class AttemptsTable(BaseTable):
    def __init__(self, parent, rows, **kwargs):
        super().__init__(
            parent,
            title_key='guessed_chars',
            columns=3,
            rows=rows
        )
        self.headers = ["Char", "Attempt", "Binary"]

        self.set_placeholder('table_placeholder')
        self.init()

    def reset_table(self):
        self.reset()

    def init(self):
        """ Initialize the table """
        self.data = [self.headers]
        self.update_table()

    def add_char(self, char, attempt):
        alphabet_len = len(self.localisation.get_alphabet())

        binary = ['-'] * alphabet_len
        if attempt <= alphabet_len:
            binary[attempt - 1] = '1'

        binary_string = ''.join(binary)
        symbol = f'Symbol:\t{char}\nAttempt:\t{attempt}\n{binary_string}'

        self.data.append([symbol])
        self.update_table()
