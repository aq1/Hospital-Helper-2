# -*- coding: UTF-8 -*-

import os
import sys

from PyQt5 import QtCore
from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QDesktopWidget, QVBoxLayout,
                             QTextEdit, QGridLayout, QApplication, QHBoxLayout,
                             QFormLayout, QStyle, QShortcut, QStyle, QStyleOption,
                             QFrame, QPushButton, QScrollArea, QStackedLayout, QGridLayout)

from PyQt5.QtGui import (QKeySequence, QFont, QFontDatabase, QPainter)


class TopSystemButtons(QFrame):
    """
    Frame contains close and minimize buttons
    """

    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window

        b = QHBoxLayout()
        b.addStretch()
        b.setSpacing(0)
        b.setContentsMargins(0, 0, 0, 0)

        exit_button = QPushButton('x')
        exit_button.clicked.connect(QCoreApplication.instance().quit)

        minimize_button = QPushButton('_')
        minimize_button.clicked.connect(self.minimize)

        b.addWidget(minimize_button)
        b.addSpacing(1)
        b.addWidget(exit_button)
        self.setLayout(b)

    def minimize(self, event):
        QWidget().setWindowState(Qt.WindowMinimized)


class TopFrame(QFrame):
    """
    Top Frame with decorative elements
    """

    pass


class Input(QFrame):

    """
    Input contains QLabel and QLineEdit
    """

    def __init__(self, label_text):
        super().__init__()
        hbox = QHBoxLayout()
        hbox.addWidget(QLabel(_(label_text)))
        hbox.addStretch()
        e = QLineEdit()
        e.setAlignment(Qt.AlignRight)
        e.setFixedWidth(170)

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
        hbox.addSpacing(self.width() * 0.15)
        # grid = QGridLayout()
        # grid.setOriginCorner(Qt.TopLeftCorner)

        # col = -2
        rows = 5
        for i, arg_name in enumerate(item):
            if i % 5 == 0:
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

        QShortcut(QKeySequence('Esc'), self).activated.connect(QCoreApplication.instance().quit)


class MainWindow(QWidget):

    def __init__(self, items):
        super().__init__()

        self.items = items

        self.stacked_layout = QStackedLayout()

        vbox = QVBoxLayout()
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(0)
        vbox.addWidget(TopSystemButtons(self), stretch=3)
        vbox.addWidget(TopFrame(), stretch=15)
        vbox.addSpacing(40)
        vbox.addLayout(self.stacked_layout, stretch=40)
        self.setLayout(vbox)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setWindowTitle('Hospital Helper')
        dw = QDesktopWidget()
        w = dw.geometry().size().width() * 0.75
        self.resize(w, w * 0.6)

        qr = self.frameGeometry()
        cp = dw.availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        self._create_layout()

        self.i = 0
        self.show()

    def mousePressEvent(self, event):
        self.i = (self.i + 1) % len(self.items)
        self.stacked_layout.setCurrentIndex(self.i)

    def _create_layout(self):

        for item in self.items:
            frame = AttributesFrame(main_window=self, item=item)
            self.stacked_layout.addWidget(frame)

    def close(self, event=None):
        QCoreApplication.instance().quit

    def mimnimize(self, event=None):
        self.setWindowState(Qt.WindowMinimized)


def init(items):
    app = QApplication(sys.argv)
    with open(os.path.join(os.path.dirname(__file__), 'style.qss'), 'r') as f:
        app.setStyleSheet(f.read())
    mw = MainWindow(items)
    sys.exit(app.exec_())
