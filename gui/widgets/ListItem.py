import customtkinter as ctk
from gui.frames.BaseFrame import BaseFrame

from styles.colors import *
from styles.font import *
from styles.padding import *


class ListItem(BaseFrame):
    def __init__(self,
                 parent,
                 data,
                 is_odd=False,
                 **kwargs
                 ):
        """
        A list item to display data in the structured fromat.
        :param parent: Parent widget.
        :param data: A dict or tuple containing data to display
        :param is_odd: Determines the background (for row alternating)
        """

        super().__init__(parent, **kwargs)

        self.data = data

        color1 = ctk.ThemeManager.theme["CTk"]["fg_color"]
        color2 = ctk.ThemeManager.theme["CTkFrame"]["top_fg_color"]

        fg_color = color2 if is_odd else color1
        self.configure(fg_color=fg_color)

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.rowconfigure((0, 1), weight=1)

        leading_key = self.data['leading'].get('key', None)
        leading_value = self.data['leading'].get('value', None)

        self.leading = ctk.CTkLabel(
            self,
            height=text_small_height,
            font=ctk.CTkFont(
                family=font,
                size=text_small
            )
        )
        self.localisation.bind(
            self.leading,
            leading_key,
            lambda text: self.update_leading(text, leading_value)
        )
        self.leading.grid(row=0, column=0, sticky='w', padx=pad_2, pady=(pad_2, pad_0))

        trailing_key = self.data['trailing'].get('key', None)
        trailing_value = self.data['trailing'].get('value', None)
        self.trailing = ctk.CTkLabel(
            self,
            height=text_small_height,
            font=ctk.CTkFont(
                family=font,
                size=text_small
            )
        )
        self.localisation.bind(
            self.trailing,
            trailing_key,
            lambda text: self.update_trailing(text, trailing_value)
        )
        self.trailing.grid(row=0, column=1, sticky='w', pady=(pad_2, pad_0))

        sub_value = self.data['sub'].get('value', None)
        self.sub = ctk.CTkLabel(
            self,
            text=sub_value,
            font=ctk.CTkFont(
                family=font,
                size=text_small
            )
        )
        self.sub.grid(row=1, column=0, columnspan=2, sticky='w', padx=pad_2, pady=(pad_0, pad_2))

    def update_leading(self, text, value):
        self.leading.configure(text=f"{text}: {value}")

    def update_trailing(self, text, value):
        self.trailing.configure(text=f"{text}: {value}")

    def update_sub(self, value):
        self.sub.configure(text=value)
