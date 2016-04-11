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

        l = QLabel(_(model.__table__.name))
        l.setObjectName('title')
        layout.addWidget(l)

        for row in self._get_rows(model):
            for w in row:
                layout.addWidget(w)

        self.setGraphicsEffect(self._get_shadow())

        hbox = QHBoxLayout()
        hbox.addSpacing(30)

        for l, n, f in zip((' Сохранить', ' Закрыть'), ('save', 'close'), (self._save, parent.deleteLater)):
            b = QPushButton(l)
            b.clicked.connect(f)
            b.setObjectName(n)
            # b.setGraphicsEffect(self._get_shadow())
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
        self.setFixedHeight(parent.main_window.height() - 200)
        self.move((parent.width() - self.width()) / 2, (parent.height() - self.height()) / 2)
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
                items = [str(i) for i in items]
                widget = QComboBox()
                widget.addItems(items)
                widget.currentIndexChanged.connect(self._check_input)
            else:
                widget = QLineEdit()
                widget.textEdited.connect(self._check_input)

            widget.setObjectName(column.name)
            yield QLabel(_(label)), widget

    def _save(self, event=None):
        kwargs = {}
        for each in self.findChildren(QLineEdit):
            kwargs[each.objectName()] = each.text()

        for each in self.findChildren(QComboBox):
            kwargs[each.objectName()] = self.foreigns[each.objectName()][each.currentIndex()].id

        instance = self.model(**kwargs)
        db.save(instance)
        self.callback(instance)

    def _get_shadow(self):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        return shadow

    def _check_input(self):
        self.findChild(QPushButton, name='save').setDisabled(
            not all([each.text() for each in self.findChildren(QLineEdit)]))
