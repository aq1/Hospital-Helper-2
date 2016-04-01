import functools

from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import (QWidget, QFrame, QLabel, QHBoxLayout, QRadioButton,
                             QVBoxLayout, QPushButton, QGraphicsDropShadowEffect,
                             QLineEdit, QFormLayout, QStackedLayout, QScrollBar, QScroller,
                             QGroupBox, QScrollArea)


class ReportTypeSelectWidget(QWidget):

    TEMPLATES_PER_LINE = 3

    def __init__(self, item_widget, items, templates):
        super().__init__()

        self.item_widget = item_widget
        self.layout = QStackedLayout()
        self.setLayout(self.layout)

        for i, item in enumerate(items):
            self.layout.addWidget(self._create_and_get_scroll(i, templates[item.id]))

    def _create_and_get_scroll(self, item_index, templates):
        widget = QWidget()
        groupbox = QGroupBox()
        vbox = QVBoxLayout()
        vbox.setSpacing(0)
        vbox.setContentsMargins(0, 0, 0, 0)

        for i, template in enumerate(templates):
            if i % self.TEMPLATES_PER_LINE == 0:
                hbox = QHBoxLayout()
                vbox.addLayout(hbox)

            b = QRadioButton(_(templates[i].name))
            b.clicked.connect(functools.partial(self._button_clicked, item_index, template))
            hbox.addWidget(b, stretch=33)

        hbox.addStretch(99 - hbox.count() * 33)
        vbox.addStretch()

        groupbox.setLayout(vbox)
        scroll = QScrollArea()
        scroll.setWidget(groupbox)
        scroll.setWidgetResizable(True)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        this_vbox = QVBoxLayout(widget)
        this_vbox.addWidget(scroll)

        return widget

    def item_selected(self, index):
        self.layout.setCurrentIndex(index)

    def _button_clicked(self, item_index, template):
        index = self.item_widget.template_selected(item_index, template)
        if index:
            self.item_selected(index)


class ReportObjectSelectWidget(QFrame):

    def __init__(self, parent, items):

        super().__init__()

        self.parent = parent
        self.items = items

        groupbox = QGroupBox()
        vbox = QVBoxLayout()
        vbox.setSpacing(0)
        vbox.setContentsMargins(0, 0, 0, 0)
        for i, item in enumerate(items):
            b = QRadioButton(_(item.name))
            b.setChecked(i == 0)
            b.toggled.connect(functools.partial(self._button_clicked, b, i))
            vbox.addWidget(b)
        vbox.addStretch()

        groupbox.setLayout(vbox)
        scroll = QScrollArea()
        scroll.setWidget(groupbox)
        scroll.setWidgetResizable(True)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        this_vbox = QVBoxLayout(self)
        this_vbox.addWidget(scroll)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        self.setGraphicsEffect(shadow)

    def _button_clicked(self, button, index):
        self.parent.item_selected(index)

    def template_selected(self, item_index, template):
        """
        Returns index of the first item without template
        that is placed after current item
        """
        self.items[item_index].template = template
        for i, each in enumerate(self.items[item_index:] + self.items[:item_index], item_index):
            if not each.template:
                index = i % len(self.items)
                buttons = self.findChildren(QRadioButton)
                buttons[item_index].setChecked(False)
                buttons[index].setChecked(True)
                return index


class ReportWidget(QFrame):

    LEFT_MARGIN = 25

    def __init__(self, main_window, items, templates):

        super().__init__()

        hbox = QHBoxLayout()
        self.setLayout(hbox)

        self.item_widget = ReportObjectSelectWidget(self, items)
        self.templates_widget = ReportTypeSelectWidget(self.item_widget, items, templates)
        hbox.addWidget(self.item_widget, stretch=25)
        hbox.addWidget(self.templates_widget, stretch=55)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        self.setGraphicsEffect(shadow)

    def item_selected(self, index):
        self.templates_widget.item_selected(index)
