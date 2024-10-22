# frames
from .BaseFrame import BaseFrame
from .ProbabilityTable import ProbabilityTable
from .AttemptsTable import AttemptsTable

from styles.padding import *


class RightFrame(BaseFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, transparent_bg=True, **kwargs)

        alphabet_len = len(self.localisation.get_alphabet())

        self.prob_table = ProbabilityTable(self, alphabet_len)
        self.add_widget(self.prob_table, side='top', pady=(pad_0, pad_2))

        self.attempts_table = AttemptsTable(self, alphabet_len)
        self.add_widget(self.attempts_table, side='bottom', pady=(pad_2, pad_0))

        self.manager.load_widgets({
            'prob_table': self.prob_table,
            'attempts_table': self.attempts_table
        })
