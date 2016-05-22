import functools

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QFrame, QPushButton, QHBoxLayout, QLabel,
                             QGridLayout, QGraphicsDropShadowEffect)

from gui import utils


class SelectMenu(QFrame):

    BUTTON_SELECTED_QSS = "color: white; padding-bottom: 23px; border-bottom: 2px solid #FFEB3B;"

    def __init__(self, main_window, items):

        super().__init__()
        self.hide()
        hbox = QHBoxLayout()
        hbox.setSpacing(0)
        hbox.setContentsMargins(0, 0, 0, 0)
        self.setLayout(hbox)

        hbox.addSpacing(25)
        main_window.communication.user_selected.connect(self._show)
        main_window.communication.menu_item_selected.connect(self._item_selected)

        self.buttons = []
        for i, text in enumerate(main_window.MENU_LABELS):
            btn = QPushButton(_(text))
            self.buttons.append(btn)
            if i == 0:
                btn.setStyleSheet(self.BUTTON_SELECTED_QSS)

            btn.clicked.connect(functools.partial(main_window.communication.menu_item_selected.emit, i))
            hbox.addWidget(btn)

        SelectItemMenu(main_window, self, items)
        self.buttons[0].setText(_(main_window.items[0].name))
        self.buttons[0].setFixedWidth(int(main_window.width() / 5))
        hbox.addStretch()

    def _item_selected(self, index):
        for each in self.buttons:
            each.setStyleSheet('')

        self.buttons[index].setStyleSheet(self.BUTTON_SELECTED_QSS)

    def _show(self, *args):
        self.show()
        self.raise_()

    def set_item_label(self, text):
        self.buttons[0].setText(_(text))


class SelectItemMenu(QFrame):

    HINTS = [(key, getattr(Qt, 'Key_{}'.format(key))) for key in '12345QWERTASDFGZXCVB']

    def __init__(self, main_window, select_menu, items):

        super().__init__(main_window)

        self._create_hints_list()
        self.items = items
        self.resize(main_window.width() * 0.6, main_window.height() * 0.4)
        self.hide()

        main_window.communication.toggle_select_item.connect(self.toggle_visibility)
        main_window.communication.set_select_item_visibility.connect(self.set_visible)
        main_window.communication.ctrl_hotkey.connect(self._show_with_hints)
        main_window.communication.resized.connect(self._move)

        grid = QGridLayout()
        self.setLayout(grid)
        grid.setSpacing(0)
        grid.setContentsMargins(0, 0, 0, 0)

        cols = 3
        self.hints_labels = []
        for i, item in enumerate(items):
            row, col = i // cols, i % cols
            b = QPushButton(_(item.name))

            b.clicked.connect(functools.partial(select_menu.set_item_label, _(item.name)))
            b.clicked.connect(functools.partial(main_window.communication.item_selected.emit, i))
            b.clicked.connect(self.hide)
            grid.addWidget(b, row, col)

            l = QLabel(self.HINTS[i][0], self)
            l.setAlignment(Qt.AlignCenter)
            l.hide()
            self.hints_labels.append(l)

        self.setGraphicsEffect(utils.get_shadow())

    def _move(self, width, waterline):
        self.move(20, waterline)

    def _create_hints_list(self):
        self.HINTS = [(key, getattr(Qt, 'Key_{}'.format(key), -1))
                      for key in '1234qwerasdfzxcv'.upper()]

    def toggle_visibility(self):
        self.setVisible(self.isHidden())
        self.raise_()

    def set_visible(self, value):
        self.setVisible(value)
        self.raise_()

    def leaveEvent(self, event):
        self.hide()

    def _show_with_hints(self, is_visible):
        for i, item in enumerate(zip(self.hints_labels, self.findChildren(QPushButton))):
            x = item[1].x() + item[1].width() - 80
            item[0].move(x, item[1].y())
            if is_visible:
                item[0].show()
            else:
                item[0].hide()
        self.setVisible(is_visible)
        self.raise_()

    def get_item_index_by_key(self, key):
        for i, hint in enumerate(self.HINTS):
            if hint[1] == key:
                return i
