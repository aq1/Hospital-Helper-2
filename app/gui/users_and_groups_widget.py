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
        self._show_crud = self._get_crud_func(main_window)
        self.showEvent = self._get_show_event(main_window)
        self.groups = []
        self.users = []
        self.selected_group_id = None

        self._create_layout()

    def _create_layout(self):
        self._groups_layout = QVBoxLayout()
        self._users_layout = QVBoxLayout()
        self._text_field = QTextEdit()

        layout = QHBoxLayout()

        groups_wrapper = QVBoxLayout()
        groups_wrapper.setSpacing(0)
        l = QLabel('Группы')
        l.setObjectName('header')
        groups_wrapper.addWidget(l)
        groups_wrapper.addWidget(utils.get_scrollable(self._groups_layout))

        users_wrapper = QVBoxLayout()
        users_wrapper.setSpacing(0)
        users_wrapper.setContentsMargins(0, 0, 0, 0)
        l = QLabel('Пользователи')
        l.setObjectName('header')
        users_wrapper.addWidget(l)
        users_wrapper.addWidget(utils.get_scrollable(self._users_layout))

        text_wrapper = QVBoxLayout()
        text_wrapper.setSpacing(0)
        l = QLabel('Заголовок')
        l.setObjectName('header')
        text_wrapper.addWidget(l)
        text_wrapper.addWidget(self._text_field)
        self._text_field.setPlaceholderText('Заголовок будет отображаться в начале шаблона')

        h = QHBoxLayout()
        h.addStretch()
        for l, i, f in zip(('Добавить пользователя', 'Сохранить', 'Удалить'),
                           ('user', 'save_w', 'delete'),
                           (functools.partial(self._show_crud, db.User), lambda e: None, lambda e: None)):
            b = QPushButton(l)
            b.setIcon(QIcon(os.path.join(options.STATIC_DIR, 'icons', i)))
            b.setObjectName('control')
            b.setGraphicsEffect(utils.get_shadow())
            b.clicked.connect(f)
            h.addWidget(b)
        text_wrapper.addLayout(h)

        for l, s in zip((groups_wrapper, users_wrapper, text_wrapper), (20, 30, 50)):
            layout.addLayout(l, stretch=s)

        self.setLayout(layout)
        self.setGraphicsEffect(utils.get_shadow())

    def _get_crud_func(self, main_window):
        def _show_crud(model, item=None):
            CrudWidget(main_window, model=model, callback=self._refresh, item=item)

        return _show_crud

    def _get_show_event(self, main_window):
        def _show_event(event=None):
            main_window.communication.action_button_toggle.emit(True, 'plus', functools.partial(self._show_crud,
                                                                                                db.Organization))
            self._refresh()

        return _show_event

    def _group_selected(self, group):
        self.selected_group_id = group.id
        utils.clear_layout(self._users_layout)
        for user in db.SESSION.query(db.User).filter(db.User.organization_id == group.id):
            layout = QHBoxLayout()
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(0)
            layout.addWidget(QLabel(str(user)))
            layout.addStretch()
            b = QPushButton()
            b.setIcon(QIcon(os.path.join(options.STATIC_DIR, 'icons', 'pencil_g')))
            b.clicked.connect(functools.partial(self._show_crud, db.User, user))
            layout.addWidget(b)
            wrapper = QWidget()
            wrapper.setLayout(layout)
            self._users_layout.addWidget(wrapper)
        self._users_layout.addStretch()

        self._text_field.setText(group.header)

    def _refresh(self, items=None):
        self.groups = db.SESSION.query(db.Organization).all()

        utils.clear_layout(self._groups_layout)
        for group in self.groups:
            b = QRadioButton(group.name)
            b.clicked.connect(functools.partial(self._group_selected, group))
            if group.id == self.selected_group_id:
                b.setChecked(True)
                self._group_selected(group)
            self._groups_layout.addWidget(b)
        self._groups_layout.addStretch()
