import functools

from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import (QWidget, QFrame, QLabel, QHBoxLayout,
                             QVBoxLayout, QPushButton, QGraphicsDropShadowEffect,
                             QLineEdit, QFormLayout, QStackedLayout, QScrollBar, QScroller,
                             QGroupBox, QScrollArea)


class ReportTypeSelectWidget(QWidget):

    SELECTED_BTN_STYLE = 'background-color: #58CACF; color: white;'
    NORMAL_BUTTON_STYLE = 'background-color: white; color: #212121'

    def __init__(self, parent, item, templates):
        super().__init__()

        self.templates = templates
        self.item = item

        vbox = QVBoxLayout()
        self.setLayout(vbox)
        vbox.setSpacing(0)
        vbox.setContentsMargins(0, 0, 0, 0)
        # self.setMinimumWidth(parent.width() * 0.1)

        l = QLabel(_(item.name))
        # l.setAlignment(Qt.AlignCenter)
        vbox.addWidget(l)
        for templ in templates:
            b = QPushButton(_(templ.name))
            b.clicked.connect(functools.partial(self._button_clicked, b, templ))
            vbox.addWidget(b)

        vbox.addStretch()

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        self.setGraphicsEffect(shadow)

    def _button_clicked(self, b, template):
        self.item.template = template
        # for each in self.findChildren(QPushButton):
            # each.setStyleSheet(self.NORMAL_BUTTON_STYLE)
        # b.setStyleSheet(self.SELECTED_BTN_STYLE)


class ReportWidget(QFrame):

    LEFT_MARGIN = 25

    def __init__(self, main_window, items, templates):

        super().__init__()

        self.main_window = main_window
        self.reportWidgets = []
        self.templates = templates

        groupbox = QGroupBox()
        hbox = QHBoxLayout()
        for item in items:
            r = ReportTypeSelectWidget(self, item, templates[item.id])
            self.reportWidgets.append(r)
            hbox.addWidget(r)

        hbox.addStretch()
        groupbox.setLayout(hbox)
        scroll = QScrollArea()
        scroll.setWidget(groupbox)
        scroll.setWidgetResizable(True)
        # scroll.set
        scroll.setFixedWidth(main_window.width())
        scroll.setFixedHeight(self.height())
        self.resizeEvent = lambda e: scroll.setFixedHeight(self.height())

        this_hbox = QHBoxLayout(self)
        this_hbox.addWidget(scroll)

    def showEvent(self, event):
        for widget in self.reportWidgets:
            widget.hide()
            for value in widget.item.values():
                if value:
                    widget.show()
