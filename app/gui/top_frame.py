import functools

from PyQt5.QtWidgets import (QFrame, QVBoxLayout, QHBoxLayout, QLabel)

from gui.top_system_buttons import TopSystemButtons
from gui.select_menu import SelectMenu
from gui import utils


class TopFrame(QFrame):
    """
    Top Frame with decorative elements
    """

    def __init__(self, main_window, items):
        super().__init__()

        vbox = QVBoxLayout()
        vbox.setSpacing(0)
        vbox.setContentsMargins(0, 0, 0, 0)
        self.setLayout(vbox)

        vbox.addWidget(TopSystemButtons(main_window))
        vbox.addStretch()
        hbox = QHBoxLayout()
        hbox.addSpacing(25)
        hbox.setSpacing(0)
        hbox.setContentsMargins(0, 0, 0, 0)
        vbox.addLayout(hbox)

        hbox.addWidget(QLabel())
        vbox.addStretch()
        vbox.addWidget(SelectMenu(main_window, items))

        self.resizeEvent = functools.partial(main_window.top_frame_resized, self)

        self.setGraphicsEffect(utils.get_shadow())

    def set_label_text(self, text):
        self.findChild(QLabel).setText(text)
