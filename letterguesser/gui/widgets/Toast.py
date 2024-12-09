"""Toast notification."""

from PyQt6.QtWidgets import QLabel, QVBoxLayout, QApplication, QFrame, QGraphicsOpacityEffect
from PyQt6.QtCore import QTimer, Qt, QPropertyAnimation, QEasingCurve


class Toast(QFrame):
    """A simple toast notification widget."""

    def __init__(
            self,
            message: str,
            duration: int = 3000,
            toasts_list: list = None,
            parent = None,
            **kwargs
    ):
        """
        Initialize the Toast notification.

        :param duration: The duration of the toast notification.
        """
        super().__init__(parent, **kwargs)

        self.fade_out_animation = None
        self.fade_in_animation = None
        self.toasts_list = toasts_list

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)

        self.label = QLabel(message)
        self.label.setObjectName("toast_label")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.label)

        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)

        self.adjustSize()
        self.fade_in()

        QTimer.singleShot(duration, self.fade_out)

    def cleanup(self):
        """Cleaning up the toast notification."""
        if self.toasts_list is not None and self in self.toasts_list:
            self.toasts_list.remove(self)
            # Update positions of remaining toasts
            for i, toast in enumerate(self.toasts_list):
                toast.update_position(i)
        self.close()

    def _get_geometry(self):
        """Return the screen geometry."""
        if self.parent():
            parent_widget = self.parent()
            while parent_widget.parent():  # Traverse up to the top-level parent
                parent_widget = parent_widget.parent()

            # Get the screen containing the parent widget
            screen = parent_widget.screen()
            if screen is None:
                screen = QApplication.primaryScreen()
            screen_geometry = screen.availableGeometry()
        else:
            screen_geometry = QApplication.primaryScreen().availableGeometry()

        return screen_geometry

    def show(self) -> None:
        """Position the toast in the center of the parent widget and display it."""
        screen_geometry = self._get_geometry()

        if self.toasts_list is not None:
            self.toasts_list.insert(0, self)
            for index, toast in enumerate(self.toasts_list):
                toast.update_position(index)
        else:
            # Position relative to the parent or screen
            if self.parent():
                parent_geometry = self.parent().geometry()
                x = parent_geometry.x() + parent_geometry.width() - self.width() - 20
                y = parent_geometry.y() + parent_geometry.height() - self.height() - 20
            else:
                x = screen_geometry.width() - self.width() - 20
                y = screen_geometry.height() - self.height() - 20

            self.move(x, y)

        super().show()

    def update_position(self, index):
        """Update position based on index in the toasts list."""
        screen_geometry = self._get_geometry()

        if self.parent():
            parent_geometry = self.parent().geometry()
            x = parent_geometry.x() + parent_geometry.width() - self.width() - 50
            y = parent_geometry.y() + parent_geometry.height() - self.height() - 50 - (
                    (self.height() + 10) * index
            )
        else:
            x = screen_geometry.width() - self.width() - 20
            y = screen_geometry.height() - self.height() - 20 - (
                    (self.height() + 10) * index
            )
        self.move(x, y)

    def fade_in(self):
        self.fade_in_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_in_animation.setDuration(500)  # Duration of fade-in in milliseconds
        self.fade_in_animation.setStartValue(0)
        self.fade_in_animation.setEndValue(1)
        self.fade_in_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.fade_in_animation.start()

    def fade_out(self):
        self.fade_out_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_out_animation.setDuration(500)  # Duration of fade-out in milliseconds
        self.fade_out_animation.setStartValue(1)
        self.fade_out_animation.setEndValue(0)
        self.fade_out_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.fade_out_animation.finished.connect(self.cleanup)
        self.fade_out_animation.start()