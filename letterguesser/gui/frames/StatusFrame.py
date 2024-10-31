from .BaseFrame import BaseFrame

from letterguesser.gui.widgets import TextBlockSegment
from letterguesser.styles.padding import pad_5


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

        self.local_blocks = {
            'status': self.status
        }


        self.manager.block_events['rebind'].subscribe(self.status_rebind)
        self.manager.block_events['reset'].subscribe(self.status_reset)

    def status_rebind(self, block_name, key):
        block = self.local_blocks.get(block_name)

        if block:
            self.status.rebind(key)

    def status_reset(self, block_name: str):
        block = self.local_blocks.get(block_name)

        if block:
            block.reset()
