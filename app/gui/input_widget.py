import functools

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QFrame, QHBoxLayout, QLabel,
                             QLineEdit, QGraphicsDropShadowEffect)


class InputWidget(QFrame):

    """
    Input contains QLabel and QLineEdit
    """

    def __init__(self, parent, label_text):
        super().__init__()

        # if label_text.startswith('_'):
        #     return

        self.label_text = label_text
        self.input = QLineEdit()

        hbox = QHBoxLayout()
        self.setLayout(hbox)
        hbox.addWidget(QLabel(_(label_text)))
        hbox.addStretch()

        self.input.setAlignment(Qt.AlignRight)
        self.input.setFixedWidth(190)
        self.input.textEdited.connect(functools.partial(parent.input_changed, label_text))

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        self.setGraphicsEffect(shadow)
        hbox.addWidget(self.input)

    def set_value(self, value):
        if value:
            self.input.setText(str(value))

    def mousePressEvent(self, event):
        self.input.setFocus()
