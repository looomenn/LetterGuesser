# frames
from .BaseFrame import BaseFrame

# widgets
from gui.widgets import TextBlockSegment

# styles
from styles.padding import *

class StatusFrame(BaseFrame):
    def __init__(self,
                 parent,
                 **kwargs
                 ):

        super().__init__(parent, **kwargs)

        self.status = TextBlockSegment(
            parent=self,
            localisation_key='status_label',
            initial_text='random_text'
        )

        self.add_widget(
            self.status,
            side='top',
            expand=False,
            fill='x',
            padx=pad_5, pady=pad_5
        )
