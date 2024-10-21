import customtkinter as ctk

from styles import *
from gui.frames.BaseFrame import BaseFrame


class InputBlock(BaseFrame):
    def __init__(self,
                 parent,
                 loc_label_key,
                 loc_placeholder_key,
                 is_disabled=False,
                 **kwargs
                 ):
        """
        Init InputBlock.
        :param parent: The parent widget.
        :param loc_label_key: Localisation key for the label.
        :param loc_placeholder_key: Localisation key for the placeholder.
        :param is_disabled: Whether the widget is disabled.
        :param kwargs: Additional keywords.
        """
        super().__init__(parent, transparent_bg=True, **kwargs)

        self.input_var = ctk.StringVar(value='')

        # label for the input
        self.label = ctk.CTkLabel(
            self,
            height=text_small_height,
            anchor='w',
            font=ctk.CTkFont(
                family=font,
                size=text_small
            )
        )

        self.localisation.bind(self.label, loc_label_key)
        self.add_widget(
            self.label,
            side='top',
            pady=(pad_0, pad_1)
        )

        self.input_field = ctk.CTkEntry(
            self,
            textvariable=self.input_var,
            height=40,
            font=ctk.CTkFont(
                family=font,
                size=text_small
            ),
        )

        self.localisation.bind(self.input_field, loc_placeholder_key, self.update_input)
        self.add_widget(
            self.input_field,
            side='top',
            pady=(pad_1, pad_0)
        )

        if is_disabled:
            self.disable_input()

        self.input_field.bind('<Return>', self.input_handler)

    def input_handler(self, event):
        self.manager.input_handler(self.get_input())

    def get_input(self):
        return self.input_var.get()

    def clear(self):
        self.input_var.set('')

    def update_input(self, new_value):
        self.input_var.set(new_value)

    def enable_input(self):
        self.input_field.configure(state='normal')
        self.input_field.configure(text_color=ctk.ThemeManager.theme['CTkEntry']['text_color'])

    def disable_input(self):
        self.input_field.focus()
        self.input_field.configure(state='disabled')
        self.input_field.configure(text_color=ctk.ThemeManager.theme['CTkEntry']['placeholder_text_color'])