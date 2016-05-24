import os
import functools

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QWidget, QFrame, QVBoxLayout, QHBoxLayout,
                             QLabel, QGridLayout, QPushButton)

import options
from model import db
from gui import utils


class DBWidget(QFrame):

    ITEMS_PER_PAGE = 50

    def __init__(self, main_window):

        """
        Widget to show data in model.
        """

        super().__init__(main_window)

        self.items = []
        self.current_items_index = 0
        self.model = db.Client
        self.columns = []
        self._columns_to_display = {'id', 'name', 'surname', 'patronymic',
                                    'user', 'age', 'examined'}
        self.layout = QGridLayout()
        self.header_layout = QGridLayout()
        self.control_layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        vbox = QVBoxLayout()
        vbox.setSpacing(0)
        vbox.addLayout(self.header_layout)
        vbox.addWidget(utils.get_scrollable(self.layout))
        vbox.addLayout(self.control_layout)
        self.setLayout(vbox)

        self.control_layout.addStretch()
        for icon, direciton in zip(('left.png', 'right.png'), (-1, 1)):
            b = QPushButton()
            b.setIcon(QIcon(os.path.join(options.STATIC_DIR, 'icons', icon)))
            b.clicked.connect(functools.partial(self._move, direciton))
            b.setObjectName(icon)
            self.control_layout.addWidget(b)
        self.setGraphicsEffect(utils.get_shadow())
        main_window.communication.action_button_toggle.emit(False, None, None)

    def showEvent(self, event):
        """
        On each show data is refreshing.
        """

        if not self.items:
            self.items = db.SESSION.query(self.model).order_by(self.model.id.desc())

        self.display_model()

    def hideEvent(self, event):
        """
        Delete db items.
        """

        self.items = None

    def display_model(self):
        """
        Clear widget and display items.
        """

        utils.clear_layout(self.layout)

        self.columns = []
        j = 0
        for c in self.model.__table__.columns:
            if c.name not in self._columns_to_display:
                continue
            self.columns.append(c.name)
            l = QLabel(_(c.name))
            l.setObjectName('header')
            self.header_layout.addWidget(l, 0, j)
            j += 1

        for i, item in enumerate(self.items[self.current_items_index:self.current_items_index + self.ITEMS_PER_PAGE], 0):
            self._add_row(i, item)

    def _move(self, direction):
        """
        Navigate between pages.
        """

        index = max(self.current_items_index + self.ITEMS_PER_PAGE * direction, 0)
        if index >= self.items.count():
            return

        self.current_items_index = index
        self.display_model()

    def _add_row(self, row_id, item):
        """
        Create row for item.
        """

        for j, c in enumerate(self.columns):
            self.layout.addWidget(QLabel(str(getattr(item, c))), row_id, j)
