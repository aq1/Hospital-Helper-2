from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QFrame, QPushButton, QLabel, QVBoxLayout)

from gui import utils


class AlertWidget(QFrame):

    """
    Wrapper for AlertWidgetContent.
    Shadows the application.
    """

    def __init__(self, main_window, text):
        super().__init__(main_window)
        self.setFixedSize(main_window.size())
        self.show()
        self.move(self.x(), main_window.top_system_frame_height)
        self.raise_()
        AlertWidgetContent(self, main_window, text)


class AlertWidgetContent(QFrame):

    def __init__(self, parent, main_window, text):

        """
        Widget for alert messages.
        """

        super().__init__(parent)

        vbox = QVBoxLayout()
        l = QLabel(text)
        l.setAlignment(Qt.AlignCenter)
        vbox.addWidget(l)
        vbox.addStretch()
        b = QPushButton('ok')
        b.clicked.connect(parent.deleteLater)
        vbox.addWidget(b)

        self.setLayout(vbox)
        self.show()
        self.raise_()
        self.move((main_window.width() - self.width()) / 2, (main_window.height() - self.height()) / 2)
        self.setGraphicsEffect(utils.get_shadow())
