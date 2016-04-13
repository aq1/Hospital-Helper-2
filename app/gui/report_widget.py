import subprocess
import functools

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QFrame, QLabel, QHBoxLayout, QRadioButton,
                             QVBoxLayout, QGraphicsDropShadowEffect, QStackedLayout,
                             QGroupBox, QScrollArea, QGridLayout)

from model import report


class ReportTypeSelectWidget(QFrame):

    TEMPLATES_PER_LINE = 3

    def __init__(self, item_widget, items, templates):
        super().__init__()

        self.item_widget = item_widget
        self.layout = QStackedLayout()
        self.setLayout(self.layout)

        for i, item in enumerate(items):
            self.layout.addWidget(self._create_and_get_scroll(i, templates[item.id]))
        self.layout.addWidget(QLabel())

    def _create_and_get_scroll(self, item_index, templates):
        widget = QWidget()
        groupbox = QGroupBox()
        grid = QGridLayout()
        grid.setSpacing(0)
        grid.setContentsMargins(0, 0, 0, 0)

        cols = 3
        for i, template in enumerate(templates):
            row, col = i // cols, i % cols

            b = QRadioButton(_(templates[i].name))
            b.clicked.connect(functools.partial(self._button_clicked, item_index, template))
            grid.addWidget(b, row, col)

        groupbox.setLayout(grid)
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
        if index is not None:
            self.item_selected(index)

    def show_event(self, event=None):
        indexes_to_show = self.item_widget.proceed_show_event_and_get_indexes()
        if indexes_to_show:
            self.layout.setCurrentIndex(indexes_to_show[0])
        else:
            self.layout.setCurrentIndex(self.layout.count() - 1)


class ReportObjectSelectWidget(QFrame):

    def __init__(self, parent, items):

        super().__init__()

        self.parent = parent
        self.items = items
        self.indexes_to_show = []
        self.no_items_to_show_label = QLabel('Нет данных')

        groupbox = QGroupBox()
        vbox = QVBoxLayout()
        vbox.setSpacing(0)
        vbox.setContentsMargins(0, 0, 0, 0)
        for i, item in enumerate(items):
            b = QRadioButton(_(item.name))
            b.setChecked(i == 0)
            b.toggled.connect(functools.partial(self._button_clicked, b, i))
            vbox.addWidget(b)

        vbox.addWidget(self.no_items_to_show_label)
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

        FIXME: Too many index word.
        Maybe i should better learn Qt or programming in general
        """
        self.items[item_index].template = template
        buttons = self.findChildren(QRadioButton)
        buttons[item_index].setText('{} - {}'.format(_(self.items[item_index].name), _(template.name)))
        begin = self.indexes_to_show.index(item_index)

        for i in self.indexes_to_show[begin:] + self.indexes_to_show[:begin]:
            if not self.items[i].template:
                buttons[item_index].setChecked(False)
                buttons[i].setChecked(True)
                return i

    def proceed_show_event_and_get_indexes(self):
        """
        Show only items that has at least one value filled
        And return indexes of those items
        FIXME: think of the better function name
        """

        self.indexes_to_show = []
        buttons = self.findChildren(QRadioButton)
        for i, item in enumerate(self.items):
            buttons[i].hide()
            buttons[i].setChecked(False)
            for value in item.values():
                if value:
                    buttons[i].show()
                    self.indexes_to_show.append(i)
                    break

        if self.indexes_to_show:
            self.no_items_to_show_label.hide()
            buttons[self.indexes_to_show[0]].setChecked(True)
        else:
            self.no_items_to_show_label.show()
        return self.indexes_to_show


class ReportWidget(QFrame):

    LEFT_MARGIN = 25
    ACTION_BTN_ICON = 'check'

    def __init__(self, main_window, items, templates):

        super().__init__()

        self.main_window = main_window
        self.items = items

        hbox = QHBoxLayout()
        self.setLayout(hbox)

        self.item_widget = ReportObjectSelectWidget(self, items)
        self.templates_widget = ReportTypeSelectWidget(self.item_widget, items, templates)
        hbox.addWidget(self.item_widget, stretch=25)
        hbox.addWidget(self.templates_widget, stretch=55)
        hbox.addStretch(10)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        self.setGraphicsEffect(shadow)

    def item_selected(self, index):
        self.templates_widget.item_selected(index)

    def showEvent(self, event):
        self.templates_widget.show_event()

    def action_btn_function(self):
        rep = report.Report([item for item in self.items if item.template], self.main_window.user)
        document = rep.render(strict_mode=True)
        document.save('/home/aq1/Documents/projects/Hospital-Helper-2/h.odt')
        subprocess.call(["xdg-open", '/home/aq1/Documents/projects/Hospital-Helper-2/h.odt'])
