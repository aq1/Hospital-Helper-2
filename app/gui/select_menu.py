import functools

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QFrame, QPushButton, QHBoxLayout, QLabel,
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

        self.buttons = []
        for i, text in enumerate(main_window.MENU_LABELS):
            btn = QPushButton(_(text))
            self.buttons.append(btn)
            if i == 0:
                btn.setStyleSheet(self.BUTTON_SELECTED_QSS)

            btn.clicked.connect(functools.partial(self.button_clicked, i))
            hbox.addWidget(btn)

        self.buttons[0].setText(_(main_window.items[0].name))
        self.buttons[0].setFixedWidth(int(self.main_window.width() / 5))
        hbox.addStretch()

    def button_clicked(self, index, event=None):
        for each in self.buttons:
            each.setStyleSheet('')

        self.buttons[index].setStyleSheet(self.BUTTON_SELECTED_QSS)

        self.main_window.select_menu_button_clicked(index)

    def set_item_label(self, text):
        self.buttons[0].setText(_(text))


class SelectItemMenu(QFrame):

    HINTS = [(key, getattr(Qt, 'Key_{}'.format(key))) for key in '12345QWERTASDFGZXCVB']

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
        self.hints_labels = []
        for i, item in enumerate(items):
            row, col = i // cols, i % cols
            b = QPushButton(_(item.name))
            b.clicked.connect(functools.partial(self.button_clicked, i))
            grid.addWidget(b, row, col)

            l = QLabel(self.HINTS[i][0], self)
            l.setAlignment(Qt.AlignCenter)
            l.hide()
            self.hints_labels.append(l)

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
        for i, item in enumerate(zip(self.hints_labels, self.findChildren(QPushButton))):
            x = item[1].x() + item[1].width() - 80
            item[0].move(x, item[1].y())
            if on:
                item[0].show()
            else:
                item[0].hide()

    def get_item_index_by_key(self, key):
        for i, hint in enumerate(self.HINTS):
            if hint[1] == key:
                return i
