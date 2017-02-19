import os
import functools

from sqlalchemy import or_

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QWidget, QFrame, QVBoxLayout, QHBoxLayout,
                             QLabel, QGridLayout, QPushButton, QSizePolicy,
                             QLineEdit)

from app import options
from app.model import db, report

from app.gui import utils


class DBWidget(QFrame):

    ITEMS_PER_PAGE = 50

    def __init__(self, main_window):

        """
        Widget to show Client model.
        """

        super().__init__(main_window)

        self.items = []
        self.current_items_index = 0
        self.model = db.Client
        self._query = db.SESSION.query(self.model).order_by(self.model.id.desc())
        self._open_report = self._get_open_report_func(main_window)
        self.columns = []
        self._columns_to_display = {'id', 'name', 'surname', 'patronymic',
                                    'user', 'age', 'examined', 'report'}
        self.layout = QGridLayout()
        self.header_layout = QGridLayout()
        self.control_layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        vbox = QVBoxLayout()
        vbox.setSpacing(0)
        vbox.addLayout(self._get_search_layout())
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

        self.showEvent = self._get_show_event(main_window)

    def _get_search_layout(self):
        hbox = QHBoxLayout()
        _input = QLineEdit()
        _input.setGraphicsEffect(utils.get_shadow())
        _input.setPlaceholderText('Поиск...')
        _input.textEdited.connect(self._filter)
        hbox.addWidget(_input)
        return hbox

    def _filter(self, query_text):
        # Since it's not really important,
        # I'll keep columns hard-coded here.
        # This motherfucking sqlaalchemy doesnt care about ilike function at all
        if query_text:
            query_text = '%{}%'.format(query_text)
            self.items = (db.SESSION.query(self.model)
                          .filter(or_(self.model.surname.like(query_text),
                                      self.model.name.like(query_text),
                                      self.model.patronymic.like(query_text)))
                          .order_by(self.model.id))
        else:
            self.items = self._query
        self.display_model()

    def _get_show_event(self, main_window):
        def showEvent(event):
            """
            On each show data is refreshing.
            """

            if not self.items:
                self.items = self._query

            self.display_model()
            main_window.communication.action_button_toggle.emit(False, '', None)

        return showEvent

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

        columns = [c.name for c in self.model.__table__.columns] + ['report']
        for c in columns:
            if c not in self._columns_to_display:
                continue
            self.columns.append(c)
            l = QLabel(_(c))
            l.setObjectName('header')
            l.setAlignment(Qt.AlignCenter)
            self.header_layout.addWidget(l, 0, j)
            j += 1

        for i, item in enumerate(self.items[self.current_items_index:self.current_items_index + self.ITEMS_PER_PAGE], 0):
            self._add_row(i, item)

        empty = QWidget()
        empty.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.layout.addWidget(empty, self.layout.rowCount(), 0)

    def _move(self, direction):
        """
        Navigate between pages.
        """

        index = max(self.current_items_index + self.ITEMS_PER_PAGE * direction, 0)
        if index >= self.items.count():
            return

        self.current_items_index = index
        self.display_model()

    @staticmethod
    def _get_open_report_func(main_window):
        def _open_report(reports):
            try:
                report.Report.open(reports[0].path)
            except (IndexError, AttributeError, FileNotFoundError):
                main_window.create_alert('Не удалось открыть отчет')
        return _open_report

    def _add_row(self, row_id, item):
        """
        Create row for item.
        """

        for j, c in enumerate(self.columns):
            if c == 'report':
                b = QPushButton()
                b.setIcon(QIcon(os.path.join(options.STATIC_DIR, 'icons', 'open.png')))
                b.clicked.connect(functools.partial(self._open_report, item.report))
                self.layout.addWidget(b, row_id, j)
            else:
                self.layout.addWidget(QLabel(str(getattr(item, c))), row_id, j)
