# frames
from .BaseFrame import BaseFrame


class RightFrame(BaseFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, transparent_bg=True, **kwargs)
