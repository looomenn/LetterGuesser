"""
BaseFrame provides a custom frame with optional title and transparency.

BaseFrame is a reusable frame that includes support for a title and optional
transparency, serving as a foundational frame for other frames. It also
provides access to core application instances, such as localisation,
experiment manager, and logger, which are passed through this frame for
consistent use across the application.
"""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout

from letterguesser.context import localisation, logger, manager
from letterguesser.styles.padding import pad_0, pad_4


class BaseFrame(QWidget):
    """
    Custom frame with title, transparency, and access to core app instances.

    BaseFrame allows child frames to inherit standard UI properties and access
    key application instances (`localisation`, `manager`, `logger`), ensuring
    consistent settings and centralized configuration.
    """

    def __init__(
            self,
            parent,
            title_key: str = None,
            transparent_bg: bool = False,
            **kwargs
    ):
        """
        Initialize BaseFrame with title, transparency, and core instances.

        :param parent: Parent tkinter object for the frame.
        :param title_key: Localisation key for the frame title.
        :param transparent_bg: Enables transparent background if True.
        """
        super().__init__(parent, **kwargs)

        if transparent_bg:
            self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # core instances
        self.localisation = localisation
        self.manager = manager
        self.log = logger

        # layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(pad_0, pad_0, pad_0, pad_0)
        self.layout.setSpacing(pad_4)

        self.title_label = None
        if title_key:
            self.title_label = QLabel(self)
            self.localisation.bind(self.title_label, title_key)
            self.title_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
            self.layout.addWidget(self.title_label)

    def add_widget(
            self,
            widget: QWidget,
            stretch: int = 0,
            alignment: Qt.AlignmentFlag | None = None,
            margin: tuple[int, int, int, int] = None
    ) -> None:
        """
        Add a widget to the frame with specified packing options.

        :param widget: Widget to add to the frame.
        :param stretch: Stretch factor for the widget.
        :param alignment: Alignment for the widget (Qt alignment flags).
        :param margin: Optional margins to apply (left, top, right, bottom).
        """
        if margin:
            widget.setContentsMargins(*margin)
        self.layout.addWidget(widget, stretch=stretch, alignment=alignment)


__all__ = ['BaseFrame', 'localisation']
