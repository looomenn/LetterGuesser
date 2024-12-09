"""
RightFrame displaying probability and attempts tables.

Contains frames for probability and attempt tracking in a vertical layout.
"""

from typing import Any

from .Table import Table

from PyQt6.QtWidgets import QFrame, QHBoxLayout
from letterguesser.context import localisation, manager, logger


class RightFrame(QFrame):
    """Frame with probability and attempts tables."""

    def __init__(self, **kwargs):
        """
        Initialize RightFrame with probability and attempts tables.

        :param kwargs: Additional keyword arguments for frame configuration.
        """
        super().__init__(**kwargs)

        self.manager = manager
        self.localisation = localisation
        self.logger = logger

        alphabet_len = len(self.localisation.get_alphabet())

        self.layout = QHBoxLayout(self)
        self.layout.setSpacing(16)

        self.prob_table = Table(
            'probability',
            ['attempt', 'probability'],
            row_count=alphabet_len,
            autofill={
                0: (1, int),
                1: (0,)
            }
        )
        self.layout.addWidget(self.prob_table)

        self.attempts_table = Table(
            'guessed_chars',
            ['attempt', 'char', 'value']
        )
        self.layout.addWidget(self.attempts_table)

        self.manager.table_events['reset'].subscribe(self.table_reset)
        self.manager.table_events['update'].subscribe(self.table_update)
        self.manager.table_events['init'].subscribe(self.table_init)

    def table_update(
            self,
            table_name: str,
            update_method: str,
            *args: Any,
            **kwargs: Any
    ) -> None:
        """Update specified table using the given method and parameters."""

        self.logger.debug(f'table_update called with {table_name=}, '
                          f'{update_method=}, args={args=}, kwargs={kwargs=}')

        if hasattr(self, table_name):
            table = getattr(self, table_name)

            if hasattr(table, update_method):
                method = getattr(table, update_method)

                if callable(method):
                    try:
                        method(*args, **kwargs)
                        self.logger.debug(f'Successfully called {update_method} on {table_name}')
                    except Exception as e:
                        self.logger.error(f'Error calling {update_method} on {table_name}: {e}')
        else:
            self.logger.warning(f'no such table')

    def table_reset(self, table_name: str) -> None:
        """Reset the specified table by name if it has reset() method."""
        if hasattr(self, table_name):
            table = getattr(self, table_name)

            table.reset()

    def table_init(self, table_name: str) -> None:
        """Init the specified table by name if it has an init() method."""
        if hasattr(self, table_name):
            table = getattr(self, table_name)

            if hasattr(table, 'init'):
                table.init()
