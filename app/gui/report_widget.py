import functools

from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import (QWidget, QFrame, QLabel, QHBoxLayout, QRadioButton,
                             QVBoxLayout, QPushButton, QGraphicsDropShadowEffect,
                             QLineEdit, QFormLayout, QStackedLayout, QScrollBar, QScroller,
                             QGroupBox, QScrollArea)


class ReportTypeSelectWidget(QWidget):

    TEMPLATES_PER_LINE = 3

    def __init__(self, parent, items, templates):
        super().__init__()

        self.layout = QStackedLayout()
        self.setLayout(self.layout)

        for item in items:
            self.layout.addWidget(self._create_and_get_scroll(templates[item.id]))

    def _create_and_get_scroll(self, templates):
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


class ReportWidget(QFrame):

    LEFT_MARGIN = 25

    def __init__(self, main_window, items, templates):

        super().__init__()

        hbox = QHBoxLayout()
        self.setLayout(hbox)

        self.templates_widget = ReportTypeSelectWidget(self, items, templates)
        hbox.addWidget(ReportObjectSelectWidget(self, items), stretch=25)
        hbox.addWidget(self.templates_widget, stretch=55)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        self.setGraphicsEffect(shadow)

    def item_selected(self, index):
        self.templates_widget.item_selected(index)
