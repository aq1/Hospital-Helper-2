import functools

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QWidget, QFrame, QVBoxLayout, QHBoxLayout,
                             QLabel, QGridLayout, QGraphicsDropShadowEffect,
                             QGroupBox, QScrollArea, QPushButton, QScrollBar)

from model import db


class DBWidget(QFrame):

    # ACTION_BTN_ICON = 'plus'
    ITEMS_PER_PAGE = 100

    def __init__(self, main_window):

        super().__init__()

        self.items = []
        self.current_items_index = 0
        self.model = db.Client
        self.columns = []
        self._columns_to_display = {'id', 'name', 'surname', 'patronymic',
                                    'user', 'age', 'examined'}
        self.layout = QGridLayout()
        self.header_layout = QGridLayout()
        self.control_layout = QHBoxLayout()
        content_widget = QWidget()
        # content_widget.setLayout(self.layout)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        vbox = QVBoxLayout()
        vbox.setSpacing(0)
        vbox.addLayout(self.header_layout)
        vbox.addWidget(content_widget)
        # vbox.addStretch()
        vbox.addLayout(self.control_layout)
        self.setLayout(vbox)

        groupbox = QGroupBox()

        groupbox.setLayout(self.layout)
        scroll = QScrollArea()
        scroll.setWidget(groupbox)
        scroll.setWidgetResizable(True)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        this_vbox = QVBoxLayout(content_widget)
        this_vbox.addWidget(scroll)

        self.control_layout.addStretch()
        for icon, direciton in zip(('left', 'right'), (-1, 1)):
            b = QPushButton()
            b.setIcon(QIcon('gui/static/icons/{}.png'.format(icon)))
            b.clicked.connect(functools.partial(self._move, direciton))
            b.setObjectName(icon)
            self.control_layout.addWidget(b)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        self.setGraphicsEffect(shadow)

    def showEvent(self, event):
        if not self.items:
            self.items = db.SESSION.query(self.model).order_by(self.model.id.desc())

        self.display_model()

    def display_model(self):
        self._clear_layout()

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
        index = max(self.current_items_index + self.ITEMS_PER_PAGE * direction, 0)
        # if direction < 0:
        #     quantity = (db.SESSION.query(self.model)
        #                 .filter(self.model.id < self.items[0].id).count())
        #     items = (db.SESSION.query(self.model)
        #              .filter(self.model.id < self.items[0].id)
        #              .order_by(self.model.id).offset(quantity - self.ITEMS_PER_PAGE))
        # else:
        #     items = (db.SESSION.query(self.model)
        #              .filter(self.model.id > self.items[-1].id)
        #              .order_by(self.model.id)
        #              .limit(self.ITEMS_PER_PAGE))

        # if not items.count():
        #     return

        # print(self.findChild(QScrollBar))
        # self.findChild(QScrollBar).setValue(0)
        # self.items = items
        if index >= self.items.count():
            return

        self.current_items_index = index
        self.display_model()

    def _clear_layout(self):
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().deleteLater()

    def _add_row(self, row_id, item):
        for j, c in enumerate(self.columns):
            self.layout.addWidget(QLabel(str(getattr(item, c))), row_id, j)

    def action_btn_function(self):
        print('db')
