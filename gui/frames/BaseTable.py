
import customtkinter as ctk
from CTkTable import *
from .BaseScrollFrame import BaseScrollFrame

from styles import *


class BaseTable(BaseScrollFrame):
    def __init__(self,
                 parent,
                 title_key,
                 columns,
                 rows,
                 **kwargs
                 ):
        super().__init__(parent, title_key=title_key, **kwargs)

        self.data = []

        self.table = CTkTable(self, row=rows, column=columns, corner_radius=8)
        self.table.pack_forget()

    def update_table(self):
        if not self.data:
            self.show_placeholder()
            self.table.pack_forget()
        else:
            self.hide_placeholder()
            self.table.update_values(self.data)
            self.table.pack(fill='x', expand=True, padx=pad_3, pady=(pad_2, pad_3))

    def reset(self):
        self.data = []
        self.update_table()

    def set_data(self, new_data):
        self.data = new_data
        self.update_table()
