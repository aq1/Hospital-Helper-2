# import functools
from PyQt5.QtWidgets import QGraphicsDropShadowEffect, QPushButton


class ActionButton(QPushButton):

    def __init__(self, main_window):
        super().__init__(main_window)

        self.main_window = main_window
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(5)
        self.setGraphicsEffect(shadow)

        self.move(1300, 210)
        self.clicked.connect(self._clicked)

    def _clicked(self, event):

        print('www')

    def _define_click(self, function):
        self._clicked.connect(function)
