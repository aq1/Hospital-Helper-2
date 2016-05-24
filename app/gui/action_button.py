# import functools
import os

from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QIcon

import options
from gui import utils


class ActionButton(QPushButton):

    """
    Main button for application.
    Changes callback and icon, depending on current state.
    """

    ICONS = {each.split('.')[0]: os.path.join(options.STATIC_DIR, 'icons', each)
             for each in os.listdir(os.path.join(options.STATIC_DIR, 'icons'))}

    def __init__(self, main_window):
        """
        Connect signals.
        Hide the button, it will be shown only when required signals are emited
        """
        super().__init__(main_window)
        self.hide()

        self.setGraphicsEffect(utils.get_shadow())
        main_window.communication.resized.connect(self._move)
        main_window.communication.action_button_toggle.connect(self.toggle_state)

    def _move(self, width, waterline):
        """
        Move the button when application is resized.
        """
        self.move(width - self.width() * 1.5, waterline - self.height() / 2)
        self.raise_()

    def toggle_state(self, is_visible, icon, function):
        """
        Hide/show the button.
        Change icon.
        Change callback.
        """

        if not is_visible:
            self.hide()
            return

        self.setIcon(QIcon(self.ICONS[icon]))
        try:
            self.clicked.disconnect()
        except TypeError:
            pass
        self.clicked.connect(function)

        self.show()
        self.raise_()
