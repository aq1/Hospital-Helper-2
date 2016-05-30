import functools

from PyQt5.QtWidgets import (QFrame, QHBoxLayout, QStackedLayout,
                             QVBoxLayout, QPushButton)

from gui import utils
from gui.template_widget import TemplateWidgetInOptions


class OptionsWidget(QFrame):

    """
    Widget holds menu with all options.
    """

    def __init__(self, main_window, items):

        super().__init__()

        self.items = items

        self.layout = QStackedLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self._get_menu_layout())
        self._create_layout(main_window)
        self._hide_action_button = lambda: main_window.communication.action_button_toggle.emit(False, None, None)

    def set_current_index(self, index):
        self.layout.setCurrentIndex(index)
        if not index:
            self._hide_action_button()

    def showEvent(self, event):
        if not self.layout.currentIndex():
            self._hide_action_button()

    def _get_menu_layout(self):

        rows = 8
        cols = 4
        vboxes = [QVBoxLayout() for _ in range(cols)]

        for i, name in enumerate(('Шаблоны', 'Заглушка')):
            b = QPushButton(name)
            b.clicked.connect(functools.partial(self.layout.setCurrentIndex, i + 1))
            b.setGraphicsEffect(utils.get_shadow())
            vboxes[(i // rows) % cols].addWidget(b)

        wrapper = QHBoxLayout()
        for each in vboxes:
            each.addStretch()
            wrapper.addLayout(each, stretch=int(100 / cols))
        return utils.get_scrollable(wrapper)

    def _create_layout(self, main_window):
        self.layout.addWidget(TemplateWidgetInOptions(main_window, self.items, self))
