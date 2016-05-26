from PyQt5.QtCore import Qt, QPropertyAnimation, QPoint, QTimer
from PyQt5.QtWidgets import QFrame, QLabel, QVBoxLayout

from gui import utils


class MessageWidget(QFrame):

    """
    Displays message that disappears after some time.
    """

    LEFT_MARGIN = 20
    TIMEOUT = 5000

    def __init__(self, main_window):
        super().__init__(main_window)

        vbox = QVBoxLayout()
        self.setLayout(vbox)
        vbox.setContentsMargins(0, 0, 0, 0)
        l = QLabel()
        l.setAlignment(Qt.AlignCenter)
        vbox.addWidget(l)

        self.setGraphicsEffect(utils.get_shadow())

        main_window.communication.set_message_text.connect(self._get_set_text_func(l))
        w = main_window.width() / 5
        self.setFixedSize(w, w * 0.3)
        self.move(self.LEFT_MARGIN, main_window.height())
        self.hide()

        self.show_animation = QPropertyAnimation(self, b'pos')
        self.show_animation.setStartValue(QPoint(self.LEFT_MARGIN, main_window.height()))
        self.show_animation.setEndValue(QPoint(self.LEFT_MARGIN, main_window.height() - self.height()))
        self.show_animation.setDuration(200)
        self.show_animation.finished.connect(self._set_timeout_to_hide)

        self.hide_animation = QPropertyAnimation(self, b'pos')
        self.hide_animation.setStartValue(QPoint(self.LEFT_MARGIN, main_window.height() - self.height()))
        self.hide_animation.setEndValue(QPoint(self.LEFT_MARGIN, main_window.height()))
        self.hide_animation.finished.connect(self.hide)
        self.show_animation.setDuration(200)

        self.timer = QTimer(self)

    def _get_set_text_func(self, label):
        def _set_text(text):
            self.timer.stop()
            self.show()
            self.raise_()
            label.setText(text)
            self.show_animation.start()

        return _set_text

    def _set_timeout_to_hide(self):
        self.timer.timeout.connect(self._hide)
        self.timer.start(self.TIMEOUT)

    def _hide(self, callback=None):
        if callback:
            self.hide_animation.finished.connect(callback)
            self.hide_animation.finished.connect(self.hide)
        self.hide_animation.start()
