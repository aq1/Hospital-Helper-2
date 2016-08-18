import functools

from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QStackedLayout,
                             QVBoxLayout, QPushButton)

from app.gui import utils
from app.gui.template_widget import TemplateWidgetInOptions
from app.gui.users_and_groups_widget import UsersAndGroupsWidget


class OptionsWidget(QWidget):

    """
    Widget holds menu with all options.
    """

    def __init__(self, main_window, items):

        super().__init__()

        self.items = items

        self.layout = QStackedLayout()
        self._switch_user = self._get_switch_user_func(main_window)
        self.setLayout(self.layout)
        self._hide_action_button = lambda: main_window.communication.action_button_toggle.emit(False, '', None)

        self._create_layout(main_window)

    def set_current_index(self, index):
        self.layout.setCurrentIndex(index)
        if not index:
            self._hide_action_button()

    def showEvent(self, event):
        if not self.layout.currentIndex():
            self._hide_action_button()

    def _get_switch_user_func(self, main_window):
        def _switch_user():
            main_window.menu_btn_clicked(main_window.user_frame_index)
            self.layout.setCurrentIndex(0)
        return _switch_user

    def _create_layout(self, main_window):

        wrapper = QHBoxLayout()
        self.layout.addWidget(utils.get_scrollable(wrapper))
        rows = 8
        cols = 3
        vboxes = [QVBoxLayout() for _ in range(cols)]

        widgets = ((TemplateWidgetInOptions(main_window, self.items, self), 'Шаблоны'),
                   (UsersAndGroupsWidget(main_window, self), 'Пользователи и группы'),
                   (self._switch_user, 'Сменить пользователя'),
                   )

        for i, widget in enumerate(widgets):
            b = QPushButton(widget[1])

            if callable(widget[0]):
                b.clicked.connect(widget[0])
            else:
                b.clicked.connect(functools.partial(self.layout.setCurrentIndex, i + 1))
                self.layout.addWidget(widget[0])

            b.setGraphicsEffect(utils.get_shadow())
            vboxes[(i // rows) % cols].addWidget(b)

        for each in vboxes:
            each.addStretch()
            wrapper.addLayout(each, stretch=int(100 / cols))
