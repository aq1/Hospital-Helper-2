import functools

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QFrame, QPushButton, QHBoxLayout,
                             QGridLayout, QGraphicsDropShadowEffect)


class SelectMenu(QFrame):

    BUTTON_SELECTED_QSS = "color: white; padding-bottom: 23px; border-bottom: 2px solid #FFEB3B;"

    def __init__(self, main_window):

        super().__init__()
        self.main_window = main_window

        hbox = QHBoxLayout()
        hbox.setSpacing(0)
        hbox.setContentsMargins(0, 0, 0, 0)
        self.setLayout(hbox)

        hbox.addSpacing(25)
        self.buttons = [QPushButton(_(text))
                        for text in main_window.MENU_LABELS]

        for i, btn in enumerate(self.buttons):
            if i == 0:
                btn.setStyleSheet(self.BUTTON_SELECTED_QSS)

            btn.clicked.connect(functools.partial(self.button_clicked, btn, i))
            hbox.addWidget(btn)

        self.buttons[0].setText(_(main_window.items[0].name))
        self.buttons[0].setFixedWidth(int(self.main_window.width() / 5))
        hbox.addStretch()

    def button_clicked(self, btn, index, event=None):
        for each in self.buttons:
            each.setStyleSheet('')

        btn.setStyleSheet(self.BUTTON_SELECTED_QSS)
        self.main_window.select_menu_button_clicked(index)

    def set_item_label(self, text):
        self.buttons[0].setText(_(text))


class SelectItemMenu(QFrame):

    HINTS = list(zip('12345qwertasdfgzxcvb'.upper(),
                     (49, 50, 51, 52, 53, 81, 87, 69, 82, 84, 65, 83, 68, 70)))

    def __init__(self, main_window, items):

        super().__init__(main_window)

        self._create_hints_list()
        self.main_window = main_window
        self.items = items
        self.resize(main_window.width() * 0.6, main_window.height() * 0.4)
        self.hide()

        grid = QGridLayout()
        self.setLayout(grid)
        grid.setSpacing(0)
        grid.setContentsMargins(0, 0, 0, 0)

        cols = 3
        for i, item in enumerate(items):
            row, col = i // cols, i % cols
            b = QPushButton(_(item.name))
            b.clicked.connect(functools.partial(self.button_clicked, i))
            grid.addWidget(b, row, col)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        self.setGraphicsEffect(shadow)

    def _create_hints_list(self):
        self.HINTS = [(key, getattr(Qt, 'Key_{}'.format(key), -1))
                      for key in '1234qwerasdfzxcv'.upper()]

    def button_clicked(self, index, event=None):
        self.main_window.select_item(index)

    def leaveEvent(self, event):
        self.main_window.set_select_menu_item_visibility(False)

    def toggle_hints(self, on):
        for i, items in enumerate(zip(self.HINTS, self.findChildren(QPushButton))):
            if on:
                text = '({}) '.format(items[0][0]) + _(self.items[i].name)
            else:
                text = _(self.items[i].name)
            items[1].setText(text)

    def get_item_index_by_key(self, key):
        for i, hint in enumerate(self.HINTS):
            if hint[1] == key:
                return i
