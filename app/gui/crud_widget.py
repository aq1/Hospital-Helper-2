import functools

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QFrame, QLineEdit, QPushButton, QHBoxLayout,
                             QComboBox, QLabel, QGraphicsDropShadowEffect, QVBoxLayout,
                             QGroupBox, QScrollArea)

from model import db


class CrudWidget(QFrame):

    def __init__(self, main_window, model, callback=None, item=None):
        super().__init__(main_window)
        self.setFixedSize(main_window.size())
        self.show()
        self.main_window = main_window
        self.move(0, main_window.top_sys_btns.height())
        self.raise_()
        CrudWidgetContent(self, model, callback, item)


class CrudWidgetContent(QFrame):

    def __init__(self, parent, model, callback, item=None):

        super().__init__(parent)

        self.callback = callback
        self.values = {}
        self.foreigns = {}
        self.model = model
        self.item = item
        self.parent = parent
        self.created_items = []

        self._create_layout()

    def _get_scrollable(self, layout):
        widget = QWidget()

        groupbox = QGroupBox()
        groupbox.setLayout(layout)
        scroll = QScrollArea()
        scroll.setWidget(groupbox)
        scroll.setWidgetResizable(True)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        this_vbox = QVBoxLayout(widget)
        this_vbox.addWidget(scroll)
        this_vbox.setContentsMargins(0, 0, 0, 0)
        this_vbox.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        return widget

    def _get_controls_layout(self, layout):
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.setSpacing(0)

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
        return hbox

    def _create_layout(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(30, 10, 30, 10)
        layout.setSpacing(0)

        l = QLabel(_(self.model.__table__.name))
        l.setObjectName('title')
        layout.addWidget(l)

        scrollable = QVBoxLayout()
        for row in self._get_rows(self.model):
            for w in row:
                scrollable.addWidget(w)

        scrollable = self._get_scrollable(scrollable)

        controls_layout = self._get_controls_layout(layout)

        layout.addWidget(scrollable)
        layout.addLayout(controls_layout)

        self.show()
        self.raise_()
        # self.setFixedWidth(groupbox.width() * 2)
        # self.setFixedHeight(self.parent.main_window.height() - 200)
        self.move((self.parent.width() - self.width()) / 2,
                  (self.parent.height() - self.height()) / 2)

        self._check_input()

    def _get_combobox(self, column, relations):

        label = column.name
        if label.endswith('_id'):
            label = label[:-3]
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
        for icon, new in zip(('pencil_g', 'plus'), (False, True)):
            b = QPushButton()
            b.setObjectName('icon')
            b.setIcon(QIcon('gui/static/icons/{}.png'.format(icon)))
            b.clicked.connect(functools.partial(
                self.open_crud, foreign_model, new, combo_box))
            hbox.addWidget(b, stretch=2)
        widget.setLayout(hbox)
        return label, widget

    def _get_rows(self, model):
        """
        Default row for a form is QLabel, QLineEdit
        But for foreign fields it's QComboBox
        Maybe later I will add QCalendar for dates and etc.
        """

        for column in model.__table__.columns:
            if column.name == 'id':
                continue

            if column.foreign_keys:
                label, widget = self._get_combobox(column, model.__mapper__.relationships)
            else:
                label = column.name
                widget = QLineEdit()
                widget.textEdited.connect(self._check_input)
                widget.setObjectName(column.name)
                if self.item:
                    widget.setText(getattr(self.item, column.name, ''))

            yield QLabel(_(label)), widget

    def _close(self):
        self.callback(self.created_items)
        self.parent.deleteLater()

    def _save(self, event=None):
        kwargs = {}
        for each in self.findChildren(QLineEdit):
            kwargs[each.objectName()] = each.text()

        for each in self.findChildren(QComboBox):
            kwargs[each.objectName()] = self.foreigns[each.objectName()][
                each.currentIndex()].id

        if self.item:
            self.item.update(**kwargs)
        else:
            self.item = self.model(**kwargs)
        self.item.save()
        self.created_items.append(self.item)
        self._close()

    def _check_input(self):
        self.findChild(QPushButton, name='save').setDisabled(
            not all([each.text() for each in self.findChildren(QLineEdit)]))

    def _add_foreign_item(self, combo_box, items):
        for item in items:
            created = True
            for i, each in enumerate(self.foreigns[combo_box.objectName()]):
                if each.id == item.id:
                    self.foreigns[combo_box.objectName()][i] = item
                    combo_box.removeItem(i)
                    combo_box.insertItem(i, str(item))
                    combo_box.setCurrentIndex(i)
                    created = False
                    break
            if created:
                self.created_items.append(item)
                combo_box.addItem(str(item))
                self.foreigns[combo_box.objectName()].append(item)
                combo_box.setCurrentIndex(combo_box.count() - 1)

    def open_crud(self, model, new, combo_box):

        item = None
        if not new:
            index = combo_box.currentIndex()
            if index == -1:
                return
            item = self.foreigns[combo_box.objectName()][index]
        CrudWidget(self.parent.main_window,
                   model,
                   functools.partial(self._add_foreign_item, combo_box),
                   item)
