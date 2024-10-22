# core
import customtkinter as ctk
from gui.frames.BaseFrame import localisation

# utils
from styles import *


class OptionMenu(ctk.CTkOptionMenu):

    def __init__(
            self,
            parent,
            label_key,
            initial_value,
            values,
            command,
            **kwargs
    ):
        self.values = values
        self.loc_key = label_key

        self.localisation = localisation
        self.menu_var = ctk.StringVar(value=initial_value)

        super().__init__(
            parent,
            height=BUTTON_HEIGHT,
            width=BUTTON_WIDTH,
            command=command,
            state='normal',
            variable=self.menu_var,
            fg_color=base_surface_1,
            button_color=base_surface_1,
            text_color=text_secondary,
            button_hover_color=base_fill_1,
            values=[],
            **kwargs
        )

        self.bind('<Enter>', self.on_hover)
        self.bind('<Leave>', self.on_leave)
        self.localisation.bind(self, label_key, self.update_loc)

    def disable(self):
        self.configure(state='disabled', cursor='no')

    def enable(self):
        self.configure(state='normal', cursor='hand2')

    def on_hover(self, event):
        if self.cget('state') == 'normal':
            self.configure(fg_color=base_fill_1, text_color=text_primary, button_hover_color=base_fill_1)

    def on_leave(self, event):
        if self.cget('state') == 'normal':
            self.configure(fg_color=base_surface_1, text_color=text_secondary)

    def update_loc(self, text):
        initial_value = self.menu_var.get().split(' ')[0]
        self.menu_var.set(f'{initial_value} {text}')

        formatted_values = [f'{val} {text}' for val in self.values]
        self.configure(values=formatted_values)
