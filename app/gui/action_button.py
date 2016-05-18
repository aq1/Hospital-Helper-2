# import functools
import os

from PyQt5.QtWidgets import QGraphicsDropShadowEffect, QPushButton

from gui import utils


class ActionButton(QPushButton):

    ICONS = {each.split('.')[0]: 'gui/static/icons/{}'.format(each)
             for each in os.listdir(os.path.join(os.path.dirname(__file__), 'static', 'icons'))}

    def __init__(self, main_window):
        super().__init__(main_window)

        self.setGraphicsEffect(utils.get_shadow())
        main_window.communication.resized.connect(self._move)

    def _move(self, width, waterline):
        self.move(width - self.width() * 1.5, waterline - self.height() / 2)
        self.raise_()

    def toggle_state(self, icon, function):
        self.setStyleSheet('qproperty-icon: url({})'.format(self.ICONS[icon]))
        try:
            self.clicked.disconnect()
        except TypeError:
            pass
        self.clicked.connect(function)
