# -*- coding: UTF-8 -*-

import os
import sys

from PyQt5 import QtCore
from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QDesktopWidget, QVBoxLayout,
                             QTextEdit, QGridLayout, QApplication, QHBoxLayout,
                             QFormLayout, QStyle, QShortcut, QStyle, QStyleOption,
                             QFrame, QPushButton, QScrollArea, QStackedLayout, QGridLayout,
                             QGraphicsDropShadowEffect)

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

    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setXOffset(0)
        shadow.setYOffset(3)
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

        # self.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)
        # form = QFormLayout()
        # form.setLabelAlignment(Qt.AlignRight)
        # form.setAlignment(Qt.AlignRight)
        # form.setFormAlignment(Qt.AlignRight | Qt.AlignTop)
        # form.addRow(_(label_text), e)
        # hbox = QHBoxLayout()
        # hbox.addWidget(QLabel(label_text), stretch=20)
        # hbox.addWidget(QLineEdit(), stretch=600)

        # self.setLayout(form)
        self.setLayout(hbox)


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
        hbox.setSpacing(0)
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.addSpacing(main_window.width() * 0.08)
        # grid = QGridLayout()
        # grid.setOriginCorner(Qt.TopLeftCorner)

        # col = -2
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
                # vbox.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)
                hbox.addLayout(vbox)

            vbox.addWidget(Input(arg_name))
            # if i % rows == 0:
            #     col += 2

            # l = QLabel('%s %s' % (i % rows, col))
            # e = QLineEdit()
            # e.setText('%s %s' % (i % rows, col + 1))
            # l.setAlignment(Qt.AlignRight)

            # grid.addWidget(l, i % rows, col, Qt.AlignLeft)
            # grid.addWidget(e, i % rows, col + 1, Qt.AlignLeft)

        try:
            vbox.addStretch()
        except NameError:
            pass

        hbox.addStretch(100)
        self.setLayout(hbox)
        # vbox = QVBoxLayout()
        # vbox.setContentsMargins(0, 0, 0, 0)
        # vbox.setSpacing(0)

        # hbox = QHBoxLayout()
        # hbox.setContentsMargins(0, 0, 0, 0)
        # hbox.setSpacing(0)
        # hbox.addSpacing(self.width() * 0.15)

        # for i, x in enumerate(item):
        #     if i % 6 == 0:
        #         form = QFormLayout()
        #         form.setLabelAlignment(Qt.AlignRight)
        #         hbox.addLayout(form)
        #     e = QLineEdit()
        #     e.setAlignment(Qt.AlignRight)
        #     form.addRow(_(x), e)

        # hbox.addStretch(100)
        # hbox.addSpacing(25)
        # vbox.addWidget(TopSystemButtons(), stretch=3)
        # vbox.addWidget(TopFrame(), stretch=15)
        # vbox.addStretch(5)
        # vbox.addLayout(hbox, stretch=40)
        # self.setLayout(vbox)


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

        print(main_window.waterline)
        self.move(1300, 210)


class MainWindow(QWidget):

    def __init__(self, items):
        super().__init__()

        self.items = items
        self.stacked_layout = QStackedLayout()

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setWindowTitle('Hospital Helper')
        dw = QDesktopWidget()
        w = dw.geometry().size().width() * 0.75
        self.resize(w, w * 0.6)

        vbox = QVBoxLayout()
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(0)
        self.setLayout(vbox)

        vbox.addWidget(TopSystemButtons(self), stretch=3)

        t = TopFrame(self)
        vbox.addWidget(t, stretch=15)
        self.waterline = self.height() - t.height()

        vbox.addSpacing(50)
        vbox.addLayout(self.stacked_layout, stretch=40)

        # LeftMenu(self, items)
        ActionButton(self)

        qr = self.frameGeometry()
        cp = dw.availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        self._create_layout()

        self.i = 0

        QShortcut(QKeySequence('Esc'), self).activated.connect(self.close)
        self.show()
    # def mouseReleaseEvent(self, event):
    #     self.i = (self.i + 1) % len(self.items)
    #     self.stacked_layout.setCurrentIndex(self.i)

    def _create_layout(self):

        for item in self.items:
            frame = AttributesFrame(main_window=self, item=item)
            self.stacked_layout.addWidget(frame)

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
