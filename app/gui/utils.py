from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QGroupBox, QScrollArea, QVBoxLayout


def make_scrollable(layout):
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

    return widget
