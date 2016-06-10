import functools

from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QStackedLayout,
                             QVBoxLayout, QPushButton)

from gui import utils
from gui.template_widget import TemplateWidgetInOptions
from gui.users_and_groups_widget import UsersAndGroupsWidget


class OptionsWidget(QWidget):

    """
    Widget holds menu with all options.
    """

    def __init__(self, main_window, items):

        super().__init__()

        self.items = items

        self.layout = QStackedLayout()
        self.setLayout(self.layout)
        self._create_layout(main_window)
        self._hide_action_button = lambda: main_window.communication.action_button_toggle.emit(False, None, None)

    def set_current_index(self, index):
        self.layout.setCurrentIndex(index)
        if not index:
            self._hide_action_button()

    def showEvent(self, event):
        if not self.layout.currentIndex():
            self._hide_action_button()

    def _create_layout(self, main_window):

        wrapper = QHBoxLayout()
        self.layout.addWidget(utils.get_scrollable(wrapper))
        rows = 8
        cols = 3
        vboxes = [QVBoxLayout() for _ in range(cols)]

        widgets = ((TemplateWidgetInOptions(main_window, self.items, self), 'Шаблоны'),
                   (UsersAndGroupsWidget(main_window, self), 'Пользователи и группы'))

        for i, widget in enumerate(widgets):
            self.layout.addWidget(widget[0])
            b = QPushButton(widget[1])
            b.clicked.connect(functools.partial(self.layout.setCurrentIndex, i + 1))
            b.setGraphicsEffect(utils.get_shadow())
            vboxes[(i // rows) % cols].addWidget(b)

        for each in vboxes:
            each.addStretch()
            wrapper.addLayout(each, stretch=int(100 / cols))
