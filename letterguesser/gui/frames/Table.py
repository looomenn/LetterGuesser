"""
Frame with table.
"""

from PyQt6.QtWidgets import (
    QFrame, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt6.QtCore import Qt

from letterguesser.context import localisation, manager, logger


class Table(QFrame):
    """Reusable frame with table and label."""

    def __init__(
            self,
            loc_label_key: str,
            headers_keys: list[str],
            row_count: int = 0,
            autofill: dict[int, tuple[int, type]] = None,
            parent=None,
            **kwargs
    ):
        """
        Init table.

        :param loc_label_key: Key for the label localisation.
        :param headers_keys: Keys for the headers localisation.
        :param row_count: Number of rows in the table.
        :param autofill: Autofill config for filling.
        {column_index (int): (start_value, value_type (int/str))}
        :param parent: Parent widget.
        """
        super().__init__(parent, **kwargs)

        self.localisation = localisation
        self.manager = manager
        self.logger = logger

        self.setObjectName('Container')

        self.row_count = row_count
        self.autofill = autofill or {}

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(24)
        self.setMinimumWidth(380)

        self.headers = [""] * len(headers_keys)

        self.table = QTableWidget()
        self.table.setColumnCount(len(headers_keys))
        self.table.setHorizontalHeaderLabels(headers_keys)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        self.table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        self.table.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.label.setObjectName('FrameTitle')
        self.localisation.bind(self.label, loc_label_key)

        self.placeholder = QLabel()
        self.placeholder.setAlignment(
            Qt.AlignmentFlag.AlignTop
            | Qt.AlignmentFlag.AlignHCenter
        )
        self.placeholder.setObjectName('FramePlaceholder')
        self.localisation.bind(self.placeholder, 'table_placeholder')
        self.placeholder.hide()

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.placeholder)

        for i, key in enumerate(headers_keys):
            self.localisation.bind(
                self,
                key,
                lambda text, index=i: self.update_header(index, text)
            )

        self._toggle_placeholder()

    def init(self):
        """Reinit table."""
        self.reset()
        if self.row_count > 0:
            self.table.setRowCount(self.row_count)

    def reset(self):
        """Reset table."""
        self.table.clearContents()
        self.table.setRowCount(0)
        self._apply_autofill()
        self._toggle_placeholder()

    def update_header(self, index: int, text: str):
        """Bind headers localisation."""
        self.headers[index] = text
        self.table.setHorizontalHeaderLabels(self.headers)

    def add_row(self, row_data):
        """Append row of data to the table."""
        current_row = self.table.rowCount()
        self.table.insertRow(current_row)
        for col, value in enumerate(row_data):
            self.table.setItem(current_row, col, QTableWidgetItem(str(value)))

        self._toggle_placeholder()

    def set_cell_value(self, row: int, values: list[str | int]):
        """Set cell value."""
        if row >= self.table.rowCount():
            self.table.setRowCount(row + 1)

        for column, value in enumerate(values):
            self._insert_item(row, column, value)

        self._toggle_placeholder()

    def _toggle_placeholder(self):
        """Toggle placeholder."""
        if self.table.rowCount() == 0:
            self.placeholder.show()
            self.table.hide()
        else:
            self.placeholder.hide()
            self.table.show()

    def _apply_autofill(self):
        """Apply autofill."""
        if not self.autofill:
            return

        row_count = self.row_count
        self.table.setRowCount(row_count)

        for col, config in self.autofill.items():
            if not isinstance(col, int):
                self.logger.error(f'Column index must be an integer!')

            if len(config) == 2:
                start_value, value_type = config

                for row in range(row_count):
                    value = value_type(start_value + row) if value_type == int else str(
                        start_value
                        )
                    self._insert_item(row, col, value)

            elif len(config) == 1:
                default_value = config[0]
                for row in range(row_count):
                    self._insert_item(row, col, default_value)

            else:
                self.logger.error(f'Invalid autofill configuration. Must be either '
                                  f'(start_value, type) or (default_value,).')

    def _insert_item(self, row: int, col: int, value: str | int) -> None:
        """Make item."""
        display_value = str(value)
        if isinstance(value, str) and len(display_value) > 20:
            display_value = display_value[:5] + '...'

        item = QTableWidgetItem(str(display_value))
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.table.setItem(row, col, item)
