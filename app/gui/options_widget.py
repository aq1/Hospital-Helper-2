import functools

from PyQt5.Qt import QSpacerItem, QSizePolicy
from PyQt5.QtWidgets import (QFrame, QHBoxLayout, QLabel, QGridLayout,
                             QStackedLayout, QVBoxLayout, QPushButton,
                             QTextEdit, QWidget, QGroupBox, QScrollArea)

from gui import utils
from gui.template_widget import TemplateWidgetInOptions


class OptionsWidget(QFrame):

    """
    Widget holds menu with all options.
    """

    def __init__(self, main_window, items, *args):

        super().__init__()

        self.items = items
        self.parent = main_window

        self.layout = QStackedLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self._get_menu_layout())
        self._create_layout()

    def _get_menu_layout(self):

        grid = QGridLayout()
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setSpacing(0)

        cols = 4
        for i, name in enumerate(('Шаблоны', 'Заглушка'), 1):
            row, col = i % cols, i // cols
            b = QPushButton(name)
            b.clicked.connect(functools.partial(self.layout.setCurrentIndex, i))
            grid.addWidget(b, row, col)

        grid.addItem(QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Expanding), row + 1, col)

        hbox = QHBoxLayout()
        hbox.addWidget(utils.get_scrollable(grid))
        hbox.addStretch()
        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addStretch()
        widget = QWidget()
        widget.setLayout(vbox)
        return widget

    def _create_layout(self):
        self.layout.addWidget(TemplateWidgetInOptions(self.parent, self.items))
