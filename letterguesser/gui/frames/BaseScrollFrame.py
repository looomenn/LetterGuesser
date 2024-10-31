import customtkinter as ctk

from letterguesser.context import localisation, manager

from letterguesser.styles.padding import pad_2, pad_3
from letterguesser.styles.colors import text_secondary
from letterguesser.styles.font import (
    font,
    text_small,
    text_small_height
)


class BaseScrollFrame(ctk.CTkScrollableFrame):
    def __init__(self,
                 parent,
                 title_key=None,
                 transparent_bg=False,
                 **kwargs
                 ):
        """
        :param parent: Parent object.
        :param title_key: Localisation key for the title.
        :param kwargs: Additional keyword arguments.
        """

        super().__init__(parent, **kwargs)

        if transparent_bg:
            self.configure(fg_color='transparent')

        # connect to the global localisation instance
        self.localisation = localisation
        self.manager = manager

        self.title_label = None
        if title_key:
            self.title_label = ctk.CTkLabel(
                self,
                height=text_small_height,
                font=ctk.CTkFont(
                    family=font,
                    size=text_small
                )
            )
            self.localisation.bind(self.title_label, title_key)
            self.title_label.pack(side='top', expand=False, anchor='w', padx=pad_3, pady=(pad_3, pad_2))

        self.placeholder: ctk.CTkLabel | None = None

    def set_placeholder(self, text_key):
        if not self.placeholder:
            self.placeholder = ctk.CTkLabel(
                self,
                text_color=text_secondary,
                height=text_small,
                font=ctk.CTkFont(
                    family=font,
                    size=text_small
                )
            )

        self.localisation.bind(self.placeholder, text_key)

    def show_placeholder(self):
        if self.placeholder:
            self.placeholder.pack(pady=(100, 0), expand=True)

    def hide_placeholder(self):
        if self.placeholder:
            self.placeholder.pack_forget()
