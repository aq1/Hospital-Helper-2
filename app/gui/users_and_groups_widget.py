import os
import functools

from PyQt5.Qt import QColor, Qt, QBrush, QFont, QRegExp
from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QGuiApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QFrame, QHBoxLayout, QLabel, QStackedLayout,
                             QVBoxLayout, QPushButton, QTextEdit, QWidget,
                             QRadioButton, QLineEdit)

import options
from model import db

from gui.crud_widget import CrudWidget
from gui import utils


class UsersAndGroupsWidget(QFrame):

    """
    Provide the way to add or delete groups and also dit group name and header.
    """

    def __init__(self, main_window):
        super().__init__()

        self._groups_layout = None
        self._users_layout = None
        self._text_field = None
        self._create_layout()

        self._show_crud = self._get_crud_func(main_window)
        self.showEvent = self._get_show_event(main_window)
        self.groups = []

    def _create_layout(self):
        self._groups_layout = QVBoxLayout()
        self._users_layout = QVBoxLayout()
        self._text_field = QTextEdit()

        layout = QHBoxLayout()

        groups_wrapper = QVBoxLayout()
        groups_wrapper.addWidget(QLabel('Группы'))
        groups_wrapper.addWidget(utils.get_scrollable(self._groups_layout))

        users_wrapper = QVBoxLayout()
        users_wrapper.addWidget(QLabel('Пользователи'))
        users_wrapper.addWidget(utils.get_scrollable(self._users_layout))

        text_wrapper = QVBoxLayout()
        text_wrapper.addWidget(QLabel('Заголовок'))
        text_wrapper.addWidget(self._text_field)

        b = QPushButton('Сохранить')
        b.setIcon(QIcon(os.path.join(options.STATIC_DIR, 'icons', 'save')))
        b.setGraphicsEffect(utils.get_shadow())
        h = QHBoxLayout()
        h.addStretch()
        h.addWidget(b)
        text_wrapper.addLayout(h)

        for l, s in zip((groups_wrapper, users_wrapper, text_wrapper), (20, 30, 50)):
            layout.addLayout(l, stretch=s)

        self.setLayout(layout)

    def _get_crud_func(self, main_window, item=None):
        def _show_crud():
            CrudWidget(main_window, db.Group, callback=self._refresh, item=item)

        return _show_crud

    def _get_show_event(self, main_window):
        def _show_event(event=None):
            main_window.communication.action_button_toggle.emit(True, 'plus', self._show_crud)
            self._refresh()

        return _show_event

    def _refresh(self, items=None):
        self.groups = db.SESSION.query(db.Group).all()
