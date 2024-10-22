# core
import customtkinter as ctk
from gui.frames.BaseFrame import localisation

# utils
from styles import *


class Button(ctk.CTkButton):
    def __init__(self,
                 parent,
                 label_key: str,
                 style: str = 'default',
                 command=None,
                 is_disabled: bool = False,
                 **kwargs
                 ):
        """
        Inits Button widget.
        :param parent: The parent widget were button should be placed.
        :param loc_label_key: Localisation key for the button label.
        :param style: Variant of the button (primary, secondary, danger)
        :param command: Function to assign with button (when clicking)
        :param is_disabled: Whether the button should be disabled when from the beginning.
        :param kwargs: Additional keyword arguments.
        """
        self.localisation = localisation
        self.style = style
        self.is_disabled = is_disabled

        self.key = label_key

        # styles
        self.fg_color: str | None = None
        self.text_color: str | None = None
        self.border_color: str | None = None
        self.hover_color: str | None = None
        self.text_color_disabled: str | None = None

        super().__init__(
            parent,
            text='',
            height=BUTTON_HEIGHT,
            border_width=1,
            command=command,
            **kwargs
        )

        self.propagate(False)
        self.configure(width=BUTTON_WIDTH, height=BUTTON_HEIGHT)

        self.set_style()

        if self.is_disabled:
            self.disable()

        self.localisation.bind(
            self,
            label_key
        )

    def reset(self):
        self.localisation.bind(self, self.key)

    def set_command(self, function):
        self.configure(command=function)

    def set_style(self):
        if self.style == 'default':
            if self.is_disabled:
                self.fg_color = BUTTON_DEFAULT_FG_COLOR_DISABLED
                self.border_color = BUTTON_DEFAULT_BORDER_DISABLED
            else:
                self.fg_color = BUTTON_DEFAULT_FG_COLOR
                self.border_color = BUTTON_DEFAULT_BORDER

            self.text_color_disabled = BUTTON_DEFAULT_TEXT_DISABLED
            self.hover_color = BUTTON_DEFAULT_FG_COLOR_HOVER
            self.text_color = BUTTON_DEFAULT_TEXT

        elif self.style == 'primary':
            if self.is_disabled:
                self.fg_color = BUTTON_PRIMARY_FG_COLOR_DISABLED
                self.border_color = BUTTON_PRIMARY_BORDER_DISABLED
            else:
                self.fg_color = BUTTON_PRIMARY_FG_COLOR
                self.border_color = BUTTON_PRIMARY_BORDER

            self.text_color_disabled = BUTTON_PRIMARY_TEXT_DISABLED
            self.hover_color = BUTTON_PRIMARY_FG_COLOR_HOVER
            self.text_color = BUTTON_PRIMARY_TEXT

        elif self.style == 'danger':

            if self.is_disabled:
                self.fg_color = BUTTON_DANGER_FG_COLOR_DISABLED
                self.border_color = BUTTON_DANGER_BORDER_DISABLED
            else:
                self.fg_color = BUTTON_DANGER_FG_COLOR
                self.border_color = BUTTON_DANGER_BORDER

            self.text_color_disabled = BUTTON_DANGER_TEXT_DISABLED
            self.hover_color = BUTTON_DANGER_FG_COLOR_HOVER
            self.text_color = BUTTON_DANGER_TEXT

        self.configure(
            fg_color=self.fg_color,
            hover_color=self.hover_color,
            border_color=self.border_color,
            text_color=self.text_color,
            text_color_disabled=self.text_color_disabled
        )

    def get_state(self):
        return self.cget('state')

    def enable(self):
        self.is_disabled = False
        self.configure(state='normal')
        self.set_style()

    def disable(self):
        self.configure(state='disabled')
        self.is_disabled = True
        self.set_style()
