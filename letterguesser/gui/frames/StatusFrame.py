"""
StatusFrame for displaying application status information.

This frame shows the current status or message to the user.
"""
from typing import Optional, Callable

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame, QVBoxLayout

from letterguesser.gui.widgets import InputBlock

from letterguesser.context import localisation, manager


class StatusFrame(QFrame):
    """Frame with input fields and controls for managing user input."""

    def __init__(self, **kwargs):
        """
        Initialize InputFrame with input fields and action buttons.

        :param parent: Parent tkinter object for the frame.
        """
        super().__init__(**kwargs)

        self.setObjectName('Container')

        self.manager = manager
        self.localisation = localisation

        # layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.layout.setSpacing(24)

        self.status = InputBlock(
            localisation_key='status_label',
            placeholder_key='no_input',
            is_disabled=True
        )
        self.layout.addWidget(self.status)

        self.local_blocks = {
            'status': self.status
        }

        self.manager.block_events['rebind'].subscribe(self.status_rebind)
        self.manager.block_events['reset'].subscribe(self.status_reset)

    def status_rebind(self, block_name: str, key: str) -> None:
        """
        Rebind the status block to a new localisation key.

        :param block_name: Name of the block to rebind.
        :param key: New localisation key.
        """
        block = self.local_blocks.get(block_name)

        if block:
            self.status.rebind(key)

    def status_reset(self, block_name: str) -> None:
        """
        Reset the specified status block.

        :param block_name: Name of the block to reset.
        """
        block = self.local_blocks.get(block_name)

        if block:
            block.reset()
