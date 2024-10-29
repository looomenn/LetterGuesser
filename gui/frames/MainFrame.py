# frames
from .BaseFrame import BaseFrame
from .LeftFrame import LeftFrame
from .RightFrame import RightFrame

# utils
from styles.padding import *


class MainFrame(BaseFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, transparent_bg=True, **kwargs)

        self.left_frame = LeftFrame(self)
        self.add_widget(
            self.left_frame,
            side='left',
            fill='both',
            expand=True,
            padx=(pad_0, pad_4)
        )

        self.right_frame = RightFrame(self)
        self.add_widget(
            self.right_frame,
            side='right',
            fill='both',
            expand=True,
            padx=(pad_4, pad_0)
        )
