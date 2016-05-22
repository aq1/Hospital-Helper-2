import functools

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QFrame, QGroupBox, QVBoxLayout, QLabel,
                             QScrollArea, QRadioButton, QGraphicsDropShadowEffect,
                             QHBoxLayout, QPushButton)

from model import db
from gui import utils
from gui.crud_widget import CrudWidget


class UsersWidget(QFrame):

    ACTION_BTN_ICON = 'check'

    def __init__(self, main_window):

        super().__init__()

        self.main_window = main_window

        self.content_layout = QVBoxLayout()
        self._update_content()

        vbox = QVBoxLayout()
        vbox.addWidget(utils.get_scrollable(self.content_layout))

        hbox = QHBoxLayout()
        hbox.addStretch(25)
        hbox.addLayout(vbox, stretch=50)
        hbox.addStretch(25)
        self.setLayout(hbox)

        control_layout = QHBoxLayout()
        control_layout.setContentsMargins(0, 0, 0, 0)
        control_layout.setSpacing(0)
        b = QPushButton('Добавить')
        b.clicked.connect(functools.partial(self.create_crud_widget, db.User, self._update_content))
        control_layout.addStretch()
        control_layout.addWidget(b)
        control_layout.addStretch()
        vbox.addLayout(control_layout)
        self.setGraphicsEffect(utils.get_shadow())

    def create_crud_widget(self, base, callback=None, db_object=None):
        CrudWidget(self, base, callback, db_object)

    def _update_content(self, *args):
        utils.clear_layout(self.content_layout)
        self.users = db.SESSION.query(db.User).all()
        organizations = db.SESSION.query(db.Organization).all()

        for organization in organizations:
            self.content_layout.addWidget(self._get_label(organization))
            for user in self.users:
                if user.organization_id == organization.id:
                    self.content_layout.addWidget(self._get_radio_btn(user))

        if not self.users:
            l = QLabel('Создайте пользователей\nдля начала работы')
            l.setAlignment(Qt.AlignCenter)
            self.content_layout.addWidget(l)
        self.content_layout.addStretch()

    def _get_radio_btn(self, item):
        fullname = '{} {} {}'.format(item.surname, item.name, item.patronymic)
        b = QRadioButton(fullname)
        b.mouseDoubleClickEvent = (functools.partial(self._button_clicked, item))
        return b

    def _get_label(self, item):
        l = QLabel(item.name)
        l.setObjectName(str(item.id))
        return l

    def _button_clicked(self, user, event):
        self.main_window.user_selected(user)

    def action_btn_function(self):
        for i, b in enumerate(self.findChildren(QRadioButton)):
            if b.isChecked():
                self.main_window.user_selected(self.users[i])
                break
