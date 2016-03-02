import functools

from PyQt5.QtWidgets import (QFrame, QPushButton, QHBoxLayout,
                             QGridLayout, QGraphicsDropShadowEffect)


class SelectMenu(QFrame):

    BUTTON_SELECTED_QSS = "padding-bottom: 23px; border-bottom: 2px solid #FFEB3B;"

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
                # Data button needs special action
                btn.enterEvent = functools.partial(
                    self.main_window.set_select_menu_item_visibility, True)
                btn.setStyleSheet(self.BUTTON_SELECTED_QSS)
            else:
                btn.enterEvent = functools.partial(
                    self.main_window.set_select_menu_item_visibility, False)

            btn.clicked.connect(functools.partial(self.button_clicked, btn))
            hbox.addWidget(btn)

        hbox.addStretch()

    def button_clicked(self, btn, event=None):
        for each in self.buttons:
            each.setStyleSheet('')

        btn.setStyleSheet(self.BUTTON_SELECTED_QSS)
        self.main_window.select_menu_button_clicked(btn)


class SelectItemMenu(QFrame):

    def __init__(self, main_window, items):

        super().__init__(main_window)

        self.main_window = main_window
        self.resize(main_window.width() * 0.4, main_window.height() * 0.4)
        self.move(100, 250)
        self.hide()

        grid = QGridLayout()
        self.setLayout(grid)
        grid.setSpacing(0)
        grid.setContentsMargins(0, 0, 0, 0)

        rows = 5
        for i, item in enumerate(items):
            b = QPushButton(_(item.name))
            b.clicked.connect(functools.partial(self.button_clicked, i))
            grid.addWidget(b, i % rows, i // rows)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        self.setGraphicsEffect(shadow)

    def button_clicked(self, index, event=None):
        self.main_window.select_item(index)

    def leaveEvent(self, event):
        self.main_window.set_select_menu_item_visibility(False)