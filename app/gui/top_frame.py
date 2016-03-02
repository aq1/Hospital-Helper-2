from PyQt5.QtWidgets import (QFrame, QVBoxLayout, QHBoxLayout, 
                             QGraphicsDropShadowEffect, QLabel)

from gui.select_menu import SelectMenu


class TopFrame(QFrame):
    """
    Top Frame with decorative elements
    """

    def __init__(self, main_window, items):
        super().__init__()

        self.main_window = main_window
        vbox = QVBoxLayout()
        vbox.setSpacing(0)
        vbox.setContentsMargins(0, 0, 0, 0)
        self.setLayout(vbox)

        vbox.addStretch()
        hbox = QHBoxLayout()
        hbox.addSpacing(25)
        hbox.setSpacing(0)
        hbox.setContentsMargins(0, 0, 0, 0)
        vbox.addLayout(hbox)

        hbox.addWidget(QLabel())
        vbox.addStretch()
        vbox.addWidget(SelectMenu(main_window))

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(5)
        self.setGraphicsEffect(shadow)

    def set_label_text(self, text):
        self.findChild(QLabel).setText(text)
