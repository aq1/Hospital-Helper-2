import os
import functools

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QFrame, QHBoxLayout, QLabel, QVBoxLayout, QComboBox,
                             QPushButton, QTextEdit, QWidget, QRadioButton)

import options
from model import db

from gui.crud_widget import CrudWidget
from gui import utils


class UsersAndGroupsWidget(QFrame):
    """
    Provide the way to add or delete groups and also dit group name and header.
    """

    def __init__(self, main_window, parent):
        super().__init__()

        self._groups_combo_box = None
        self._users_layout = None
        self._text_field = None
        self.show_message = main_window.communication.set_message_text.emit
        self._show_crud = self._get_crud_func(main_window)
        self.showEvent = self._get_show_event(main_window)
        self._delete = self._get_delete_func(main_window)
        self.groups = []
        self.users = []
        self.selected_group_index = 0

        self._create_layout(parent)

    def _create_layout(self, parent):
        self._groups_combo_box = QComboBox()
        self._users_layout = QVBoxLayout()
        self._text_field = QTextEdit()

        self._text_field.setPlaceholderText('Заголовок появится в начале отчета')
        self._groups_combo_box.currentIndexChanged.connect(self._group_selected)

        layout = QHBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(20)

        right_side = QVBoxLayout()
        right_side.setContentsMargins(0, 0, 0, 0)
        right_side.setSpacing(0)
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.setSpacing(0)
        for i, f in zip(('save_w', 'delete'), (self._save, self._delete)):
            b = QPushButton()
            b.setIcon(QIcon(os.path.join(options.STATIC_DIR, 'icons', i)))
            b.setObjectName('button')
            b.setGraphicsEffect(utils.get_shadow())
            b.clicked.connect(f)
            hbox.addWidget(b)
            hbox.addSpacing(5)
        hbox.addStretch()
        right_side.addLayout(hbox)
        right_side.addSpacing(5)
        l = QLabel('Заголовок')
        l.setObjectName('text-header')
        right_side.addWidget(l)
        right_side.addWidget(self._text_field)

        left_side = QVBoxLayout()
        left_side.setContentsMargins(0, 0, 0, 0)
        left_side.setSpacing(0)
        left_side.addWidget(self._groups_combo_box)
        wrapper = QWidget()
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.setSpacing(0)
        l = QLabel('Пользователи')
        l.setObjectName('header')
        hbox.addWidget(l)
        hbox.addStretch()
        b = QPushButton()
        b.setIcon(QIcon(os.path.join(options.STATIC_DIR, 'icons', 'plus')))
        b.clicked.connect(functools.partial(self._show_crud, db.User))
        hbox.addWidget(b)
        wrapper.setLayout(hbox)
        wrapper.setObjectName('header')
        left_side.addWidget(wrapper)
        left_side.addWidget(utils.get_scrollable(self._users_layout))
        b = QPushButton('Назад')
        b.setObjectName('button')
        left_side.addSpacing(5)
        left_side.addWidget(b)

        layout.addLayout(left_side, stretch=30)
        layout.addLayout(right_side, stretch=70)
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

    def _group_selected(self, index):
        self.selected_group_index = index
        utils.clear_layout(self._users_layout)
        self._text_field.setText(self.groups[index].header)
        if not self.groups:
            self._users_layout.addStretch()
            l = QLabel('Создайте группу, чтобы добавлять пользователей.')
            l.setAlignment(Qt.AlignCenter)
            self._users_layout.addWidget(l)
            self._users_layout.addStretch()
            return

        for user in db.SESSION.query(db.User).filter(db.User.organization_id == self.groups[index].id,
                                                     db.User.deleted == False,
                                                     db.Organization.deleted == False):
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

    def _refresh(self, after_delete=False):
        self.groups = list(db.SESSION.query(db.Organization).filter(db.Organization.deleted == False))

        if after_delete:
            self.selected_group_index = 0

        self._clear_layout()
        for i, group in enumerate(self.groups):
            self._groups_combo_box.insertItem(i, str(group))

        self._group_selected(self.selected_group_index)

    def _clear_layout(self):
        utils.clear_layout(self._users_layout)
        self._text_field.setText('')
        for i in range(self._groups_combo_box.count()):
            self._groups_combo_box.removeItem(i)

    def _save(self):
        self.groups[self.selected_group_index].header = self._text_field.toPlainText()
        self.groups[self.selected_group_index].save()
        self.show_message('Ок')

    def _get_delete_func(self, main_window):
        def _delete_for_real(for_real):
            if not for_real:
                return
            self.groups[self.selected_group_index].deleted = True
            self.groups[self.selected_group_index].save()
            self._refresh(after_delete=True)
            return

        def _delete():
            main_window.create_alert(text='Действие не может быть отменено.\nПродолжить?', callback=_delete_for_real)

        return _delete
