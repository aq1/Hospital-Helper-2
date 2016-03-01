from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QFrame, QHBoxLayout, QLabel,
                             QLineEdit, QGraphicsDropShadowEffect)


class InputWidget(QFrame):

    """
    Input contains QLabel and QLineEdit
    """

    def __init__(self, label_text):
        super().__init__()

        if label_text.startswith('_'):
            return

        hbox = QHBoxLayout()
        self.setLayout(hbox)
        hbox.addWidget(QLabel(_(label_text)))
        hbox.addStretch()
        self.input = QLineEdit()
        self.input.setAlignment(Qt.AlignRight)
        self.input.setFixedWidth(200)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        self.setGraphicsEffect(shadow)
        hbox.addWidget(self.input)

    def mousePressEvent(self, event):
        self.input.setFocus()
