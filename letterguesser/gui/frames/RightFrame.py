from letterguesser.styles.padding import pad_0, pad_2
from .AttemptsList import AttemptsList
from .BaseFrame import BaseFrame
from .ProbabilityTable import ProbabilityTable


class RightFrame(BaseFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, transparent_bg=True, **kwargs)

        alphabet_len = len(self.localisation.get_alphabet())

        self.prob_table = ProbabilityTable(self, alphabet_len)
        self.add_widget(self.prob_table, side='top', pady=(pad_0, pad_2))

        self.attempts_table = AttemptsList(self)
        self.add_widget(self.attempts_table, side='bottom', pady=(pad_2, pad_0))

        self.manager.table_events['reset'].subscribe(self.table_reset)
        self.manager.table_events['update'].subscribe(self.table_update)
        self.manager.table_events['init'].subscribe(self.table_init)

    def table_update(self, table_name: str, update_method: str, *args, **kwargs) -> None:
        if hasattr(self, table_name):
            table = getattr(self, table_name)

            if hasattr(table, update_method) and callable(getattr(table, update_method)):
                method = getattr(table, update_method)
                method(*args, **kwargs)

    def table_reset(self, table_name: str) -> None:
        if hasattr(self, table_name):
            table = getattr(self, table_name)

            if hasattr(table, 'reset') and callable(getattr(table, 'reset')):
                table.reset()

    def table_init(self, table_name: str) -> None:
        if hasattr(self, table_name):
            table = getattr(self, table_name)

            if hasattr(table, 'init') and callable(getattr(table, 'init')):
                table.init()
