import functools

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QFrame, QFormLayout, QLineEdit, QPushButton, QHBoxLayout,
                             QComboBox, QLabel, QGraphicsDropShadowEffect, QVBoxLayout, QGroupBox, QScrollArea)

from model import db


class CrudWidget(QFrame):

    def __init__(self, main_window, model, callback=None, db_object=None):
        super().__init__(main_window)
        self.setFixedSize(main_window.size())
        self.show()
        self.main_window = main_window
        self.move(0, main_window.top_sys_btns.height())
        self.raise_()
        CrudWidgetContent(self, model, callback, db_object)


class CrudWidgetContent(QFrame):

    def __init__(self, parent, model, callback, db_object=None):

        super().__init__(parent)

        self.callback = callback
        self.values = {}
        self.foreigns = {}
        self.model = model
        self.parent = parent
        self.created_items = []

        widget = QWidget()
        vbox = QVBoxLayout()
        vbox.setContentsMargins(30, 0, 0, 10)
        vbox.setSpacing(0)
        self.setLayout(vbox)
        vbox.addWidget(widget)

        groupbox = QGroupBox()

        layout = QVBoxLayout()
        # layout.setContentsMargins(30, 10, 10, 10)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        l = QLabel(_(self.model.__table__.name))
        l.setObjectName('title')
        layout.addWidget(l)

        for row in self._get_rows(self.model):
            for w in row:
                layout.addWidget(w)

        layout.addStretch()
        hbox = QHBoxLayout()
        hbox.addSpacing(30)

        args = ((QGraphicsDropShadowEffect(), QGraphicsDropShadowEffect()),
                (' Сохранить', ' Закрыть'),
                ('save', 'close'),
                (self._save, self._close))

        for s, l, n, f in zip(*args):
            b = QPushButton(l)
            b.clicked.connect(f)
            b.setObjectName(n)
            s.setBlurRadius(10)
            s.setXOffset(0)
            s.setYOffset(0)
            b.setGraphicsEffect(s)
            hbox.addWidget(b)

        hbox.addStretch()
        vbox.addLayout(hbox)

        groupbox.setLayout(layout)
        scroll = QScrollArea()
        scroll.setWidget(groupbox)
        scroll.setWidgetResizable(True)
        # scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        this_vbox = QVBoxLayout(widget)
        this_vbox.addWidget(scroll)
        this_vbox.setContentsMargins(30, 10, 10, 10)
        this_vbox.setSpacing(0)

        self.show()
        self.raise_()
        self.setFixedWidth(groupbox.width() * 2)
        self.setFixedHeight(self.parent.main_window.height() - 200)
        self.move((self.parent.width() - self.width()) / 2, (self.parent.height() - self.height()) / 2)

        self._check_input()

    def _get_rows(self, model):
        """
        Default row for a form is QLabel, QLineEdit
        But for foreign fields it's QComboBox
        Maybe later I will add QCalendar for dates and etc.
        """

        relations = model.__mapper__.relationships
        for column in model.__table__.columns:
            if column.name == 'id':
                continue

            label = column.name
            if column.foreign_keys:
                if label.endswith('_id'):
                    label = column.name[:-3]
                foreign_model = relations.get(label).mapper.class_
                items = db.SESSION.query(foreign_model).all()
                self.foreigns[column.name] = items
                items_labels = [str(i) for i in items]
                widget = QWidget()
                widget.setStyleSheet('margin:0;')
                combo_box = QComboBox()
                combo_box.addItems(items_labels)
                combo_box.currentIndexChanged.connect(self._check_input)
                combo_box.setObjectName(column.name)
                hbox = QHBoxLayout()
                hbox.setContentsMargins(0, 0, 0, 0)
                hbox.setSpacing(0)
                hbox.addWidget(combo_box, stretch=95)
                # hbox.addStretch()
                b = QPushButton()
                b.setObjectName('icon')
                b.setIcon(QIcon('gui/static/icons/pencil_g.png'))
                b.clicked.connect(functools.partial(self.open_crud, foreign_model, False, combo_box, items))
                hbox.addWidget(b, stretch=2)
                b = QPushButton()
                b.setObjectName('icon')
                b.setIcon(QIcon('gui/static/icons/plus.png'))
                b.clicked.connect(functools.partial(self.open_crud, foreign_model, True, combo_box, items))
                hbox.addWidget(b, stretch=2)
                widget.setLayout(hbox)
            else:
                widget = QLineEdit()
                widget.textEdited.connect(self._check_input)
                widget.setObjectName(column.name)

            yield QLabel(_(label)), widget

    def _close(self):
        self.callback(self.created_items)
        self.parent.deleteLater()

    def _save(self, event=None):
        kwargs = {}
        for each in self.findChildren(QLineEdit):
            kwargs[each.objectName()] = each.text()

        for each in self.findChildren(QComboBox):
            kwargs[each.objectName()] = self.foreigns[each.objectName()][each.currentIndex()].id

        instance = self.model(**kwargs)
        db.save(instance)
        self.created_items.append(instance)
        self._close()

    def _check_input(self):
        self.findChild(QPushButton, name='save').setDisabled(
            not all([each.text() for each in self.findChildren(QLineEdit)]))

    def _add_foreign_item(self, combo_box, items):
        for item in items:
            self.created_items.append(item)
            combo_box.addItem(str(item))
            self.foreigns[combo_box.objectName()].append(item)

    def open_crud(self, model, new, combo_box, items):

        item = None
        if not new:
            index = combo_box.currentIndex()
            if index == -1:
                return
            item = items[index]

        CrudWidget(self.parent.main_window,
                   model,
                   functools.partial(self._add_foreign_item, combo_box),
                   item)
