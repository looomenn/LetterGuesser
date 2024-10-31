import customtkinter as ctk

from letterguesser.context import localisation, manager, logger
from letterguesser.styles.padding import pad_4


class BaseFrame(ctk.CTkFrame):
    def __init__(self,
                 parent,
                 title_key=None,
                 transparent_bg=False,
                 **kwargs
                 ):
        """
        :param parent: Where the frame should be placed (tkinter parent object)
        :param title_key: Localisation key for title
        :param kwargs: additional keyword arguments
        """

        super().__init__(parent, **kwargs)

        if transparent_bg:
            self.configure(fg_color='transparent')

        # connect to the global localisation instance
        self.localisation = localisation
        self.manager = manager
        self.log = logger

        self.title_label = None
        if title_key:
            self.title_label = ctk.CTkLabel(self, text='')
            self.localisation.bind(self.title_label, title_key)
            self.title_label.pack(side='top', anchor='w', padx=pad_4, pady=pad_4)

    def add_widget(
            self,
            widget,
            side: str = 'top',
            fill: str | None = 'both',
            expand: bool = True,
            anchor: str = 'w',
            padx: int | tuple = 0,
            pady: int | tuple = 0
    ) -> None:
        """
        Adds widgets using pack
        """
        widget.pack(side=side, fill=fill, expand=expand, anchor=anchor, padx=padx, pady=pady)
