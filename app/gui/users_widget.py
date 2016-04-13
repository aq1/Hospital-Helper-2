import functools

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QFrame, QGroupBox, QVBoxLayout, QLabel,
                             QScrollArea, QRadioButton, QGraphicsDropShadowEffect,
                             QHBoxLayout, QPushButton)

from model import db


class UsersWidget(QFrame):

    ACTION_BTN_ICON = 'check'

    def __init__(self, main_window):

        super().__init__()

        self.main_window = main_window

        groupbox = QGroupBox()

        self.vbox = QVBoxLayout()
        self.vbox.setSpacing(10)
        self.vbox.setContentsMargins(30, 30, 10, 10)

        self.users = db.SESSION.query(db.User).all()
        organizations = db.SESSION.query(db.Organization).all()

        for organization in organizations:
            self.vbox.addWidget(self._get_label(organization))
            for user in self.users:
                if user.organization_id == organization.id:
                    self.vbox.addWidget(self._get_radio_btn(user))

        self.vbox.addStretch()

        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.setSpacing(0)
        b = QPushButton('Добавить')
        b.clicked.connect(functools.partial(main_window.create_crud_widget, db.User, self.user_created))
        hbox.addStretch()
        hbox.addWidget(b)
        hbox.addStretch()
        self.vbox.addLayout(hbox)

        groupbox.setLayout(self.vbox)
        scroll = QScrollArea()
        scroll.setWidget(groupbox)
        scroll.setWidgetResizable(True)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        this_vbox = QHBoxLayout(self)
        this_vbox.addStretch(25)
        this_vbox.addWidget(scroll, stretch=50)
        this_vbox.addStretch(25)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        self.setGraphicsEffect(shadow)

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

    def user_created(self, items):
        for item in items:
            if isinstance(item, db.Organization):
                self.vbox.insertWidget(0, self._get_label(item))
            else:
                id_ = str(item.organization_id)
                for i in range(self.vbox.count()):
                    try:
                        widget_name = self.vbox.itemAt(i).widget().objectName()
                    except AttributeError:
                        continue

                    if widget_name == id_:
                        b = self._get_radio_btn(item)
                        self.vbox.insertWidget(i + 1, b)
                        break
