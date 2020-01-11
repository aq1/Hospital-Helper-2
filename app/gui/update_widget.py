import threading

from PyQt5.QtWidgets import (
    QFrame,
)

from app import updater


class UpdateWidget(QFrame):

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

    def __call__(self):
        self._update()

    def _update(self):
        self.main_window.show_message('Идет проверка обновлений')
        thread = threading.Thread(target=updater.update)
        thread.start()
