# -*- coding: UTF-8 -*-

import os
import sys
import functools

from PyQt5 import QtCore
from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QDesktopWidget, QVBoxLayout,
                             QTextEdit, QGridLayout, QApplication, QHBoxLayout,
                             QFormLayout, QStyle, QShortcut, QStyle, QStyleOption,
                             QFrame, QPushButton, QScrollArea, QStackedLayout, QGridLayout,
                             QGraphicsDropShadowEffect, QScrollArea)

from PyQt5.QtGui import (QKeySequence, QFont, QFontDatabase, QPainter)


class TopSystemButtons(QFrame):
    """
    Frame contains close and minimize buttons
    """

    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window
        self.move_offset = None

        b = QHBoxLayout()
        b.addStretch()
        b.setSpacing(0)
        b.setContentsMargins(0, 0, 0, 0)

        exit_button = QPushButton('x')
        exit_button.clicked.connect(main_window.close)

        minimize_button = QPushButton('_')
        minimize_button.clicked.connect(main_window.minimize)

        b.addWidget(minimize_button)
        b.addSpacing(1)
        b.addWidget(exit_button)
        self.setLayout(b)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(5)
        self.setGraphicsEffect(shadow)

    def mousePressEvent(self, event):
        self.move_offset = event.pos()

    def mouseReleaseEvent(self, event):
        """
        This prevents window from moving when buttons pressed
        """
        self.move_offset = None

    def mouseMoveEvent(self, event):
        if not self.move_offset:
            return

        x = event.globalX()
        y = event.globalY()
        x_w = self.move_offset.x()
        y_w = self.move_offset.y()
        self.main_window.move(x - x_w, y - y_w)


class TopFrame(QFrame):
    """
    Top Frame with decorative elements
    """

    def __init__(self, main_window, items):
        super().__init__()

        self.main_window = main_window
        vbox = QVBoxLayout()
        vbox.setSpacing(0)
        vbox.setContentsMargins(0, 0, 0, 0)
        self.setLayout(vbox)

        vbox.addStretch()
        vbox.addWidget(SelectMenu(main_window))

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(5)
        self.setGraphicsEffect(shadow)


class Input(QFrame):

    """
    Input contains QLabel and QLineEdit
    """

    def __init__(self, label_text):
        super().__init__()

        if label_text.startswith('_'):
            return

        hbox = QHBoxLayout()
        self.setLayout(hbox)
        hbox.addWidget(QLabel(_(label_text)))
        hbox.addStretch()
        e = QLineEdit()
        e.setAlignment(Qt.AlignRight)
        e.setFixedWidth(200)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        self.setGraphicsEffect(shadow)
        hbox.addWidget(e)


class AttributesFrame(QWidget):
    """
    Frame represents attributes of a single item.
    Contains form layouts - labels and inputs
    """

    def __init__(self, main_window, item):
        """
        main_window: MainWindow instance
        item: CalculableObject instance
        """

        super().__init__()
        print(item)

        self.main_window = main_window
        hbox = QHBoxLayout()
        self.setLayout(hbox)
        hbox.setSpacing(0)
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.addSpacing(25)

        rows = 5
        for i, arg_name in enumerate(item):
            if i % rows == 0:
                try:
                    vbox.addStretch(10)
                except NameError:
                    pass
                vbox = QVBoxLayout()
                vbox.setSpacing(0)
                vbox.setContentsMargins(0, 0, 0, 0)

                hbox.addLayout(vbox)

            vbox.addWidget(Input(arg_name))

        try:
            vbox.addStretch()
        except NameError:
            pass

        hbox.addStretch(100)


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
        self.buttons = [QPushButton(_(text)) for text in main_window.MENU_LABELS]

        for i, btn in enumerate(self.buttons):
            if i == 0:
                # Data button needs special action
                btn.enterEvent = self.main_window.data_button_entered
                btn.setStyleSheet(self.BUTTON_SELECTED_QSS)

            btn.clicked.connect(functools.partial(self.button_clicked, btn))
            hbox.addWidget(btn)

        hbox.addStretch()

    def button_clicked(self, btn, event=None):
        for each in self.buttons:
            each.setStyleSheet('')

        btn.setStyleSheet(self.BUTTON_SELECTED_QSS)
        self.main_window.select_menu_button_clicked(btn)


class LeftMenu(QFrame):

    def __init__(self, main_window, items):

        super().__init__(main_window)

        self.main_window = main_window
        w = main_window.width() * 0.065
        h = main_window.height() * 0.8
        self.resize(w, h)
        self.move(0, main_window.height() * 0.15)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        self.setGraphicsEffect(shadow)

        vbox = QVBoxLayout()
        self.setLayout(vbox)
        for i, each in enumerate(items):
            hbox = QHBoxLayout()
            # hbox.addWidget()
            b = QPushButton(_(each.name))
            b.clicked.connect(self.select_item)
            hbox.addWidget(b)
            vbox.addLayout(hbox)

    def select_item(self, index):
        print(index)


class ActionButton(QFrame):

    def __init__(self, main_window):
        super().__init__(main_window)

        self.main_window = main_window
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        self.setGraphicsEffect(shadow)

        # print(main_window.waterline)
        self.move(1300, 210)


class DataWidget(QFrame):

    def __init__(self, main_window, items):

        super().__init__()

        self.main_window = main_window
        self.stacked_layout = QStackedLayout()
        self.setLayout(self.stacked_layout)

        for item in items[1:]:
            frame = AttributesFrame(main_window=self, item=item)
            self.stacked_layout.addWidget(frame)


class ReportWidget(QFrame):

    def __init__(self, main_window, items):

        super().__init__()
        hbox = QHBoxLayout()
        self.setLayout(hbox)
        hbox.addWidget(QLabel('Report widget'))


class DBWidget(QFrame):

    def __init__(self, main_window, *args):

        super().__init__()
        hbox = QHBoxLayout()
        self.setLayout(hbox)
        hbox.addWidget(QLabel('DB widget'))


class OptionsWidget(QFrame):

    def __init__(self, main_window, *args):

        super().__init__()
        hbox = QHBoxLayout()
        self.setLayout(hbox)
        hbox.addWidget(QLabel('Options widget'))


class MainWindow(QWidget):

    MENU_LABELS = 'data', 'report', 'base', 'options'

    def __init__(self, items):
        super().__init__()

        self.items = items

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setWindowTitle('Hospital Helper')
        dw = QDesktopWidget()
        w = dw.geometry().size().width() * 0.75
        self.resize(w, w * 0.6)

        self.stacked_layout = QStackedLayout()
        vbox = QVBoxLayout()
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(0)
        self.setLayout(vbox)

        vbox.addWidget(TopSystemButtons(self), stretch=3)

        t = TopFrame(self, items)
        vbox.addWidget(t, stretch=15)
        self.waterline = self.height() - t.height()

        vbox.addSpacing(50)
        vbox.addLayout(self.stacked_layout, stretch=40)

        qr = self.frameGeometry()
        cp = dw.availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        self._create_layout()

        self.stack_index = 0

        self._set_shortcuts()

        self.show()

    def _set_shortcuts(self):
        QShortcut(QKeySequence('Esc'), self).activated.connect(self.close)
        QShortcut(Qt.CTRL, self).activated.connect(self.close)

    def _create_layout(self):
        # Order matters
        frames = DataWidget, ReportWidget, DBWidget, OptionsWidget
        for frame in frames:
            self.stacked_layout.addWidget(frame(self, self.items))

    def data_button_entered(self, event):
        # Event is triggered only on 'Data' tab
        if self.stack_index:
            return

        print('HAHA')

    def select_menu_button_clicked(self, btn):
        for i, each in enumerate(self.MENU_LABELS):
            if _(each) == btn.text():
                self.stack_index = i
                self.stacked_layout.setCurrentIndex(self.stack_index)

    def keyPressEvent(self, event):
        print(event.modifiers() == Qt.ControlModifier, event.text() is '')
        super().keyPressEvent(event)

    def close(self, event=None):
        QCoreApplication.instance().quit()

    def minimize(self, event=None):
        self.setWindowState(Qt.WindowMinimized)


def init(items):
    app = QApplication(sys.argv)
    with open(os.path.join(os.path.dirname(__file__), 'style.qss'), 'r') as f:
        app.setStyleSheet(f.read())
    mw = MainWindow(items)
    sys.exit(app.exec_())
