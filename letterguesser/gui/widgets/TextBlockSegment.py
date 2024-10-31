import customtkinter as ctk

from letterguesser.gui.frames.BaseFrame import BaseFrame

from letterguesser.styles.font import font, text_small, text_small_height
from letterguesser.styles.padding import pad_0, pad_1


class TextBlockSegment(BaseFrame):
    def __init__(self,
                 parent,
                 localisation_key,
                 initial_text,
                 **kwargs
                 ):
        """
        Inits TextBlock widget.
        :param parent: The parent widget.
        :param localisation_key:
        :param initial_text:
        :param kwargs:
        """
        super().__init__(parent, transparent_bg=True, **kwargs)

        self.text_var = ctk.StringVar(value=initial_text)

        self.label = ctk.CTkLabel(
            self,
            height=text_small_height,
            anchor='w',
            font=ctk.CTkFont(
                family=font,
                size=text_small
            )
        )
        self.localisation.bind(self.label, localisation_key)
        self.add_widget(
            self.label,
            side='top',
            pady=(pad_0, pad_1)
        )

        self.text_block = ctk.CTkEntry(
            self,
            textvariable=self.text_var,
            state='disabled',
            height=40,
            border_width=0
        )
        self.localisation.bind(self.text_block, 'no_input', self.update_value)

        self.add_widget(
            self.text_block,
            side='bottom',
            pady=(pad_1, pad_0)
        )

        self.text_block.configure(text_color=ctk.ThemeManager.theme['CTkEntry']['placeholder_text_color'][0])

    def rebind(self, new_loc_key: str):
        self.localisation.bind(self.text_block, new_loc_key, self.update_value)

    def update_value(self, new_value):
        self.text_var.set(new_value)

    def reset(self):
        self.localisation.bind(self.text_block, 'no_input', self.update_value)