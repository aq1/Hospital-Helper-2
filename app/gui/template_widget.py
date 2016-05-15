import functools

from PyQt5.Qt import QColor, Qt, QTextCursor
from PyQt5.QtWidgets import (QFrame, QHBoxLayout, QLabel, QGridLayout,
                             QStackedLayout, QVBoxLayout, QPushButton,
                             QTextEdit, QWidget, QGroupBox, QScrollArea,
                             QRadioButton)

from model import template

from gui import utils


class TemplateTextEdit(QTextEdit):

    BACKGROUND_COLOR = 221, 221, 221

    def __init__(self):

        super().__init__()
        self.setGraphicsEffect(utils.get_shadow())

    def keyPressEvent(self, event):

        cursor = self.textCursor()
        pos = cursor.position()
        key = event.key()
        text = self.toPlainText()
        color = self.textColor().getRgb()[:-1]

        if key == Qt.Key_Backspace and pos != 0:
            if color != (0, 0, 0):
                self._select_attribute(pos - 1)
        if key == Qt.Key_Delete and pos != len(text):
            if color != (0, 0, 0):
                self._select_attribute(pos)
            else:
                cursor.setPosition(pos + 1)
                self.setTextCursor(cursor)
                if self.textColor().getRgb()[:-1] != (0, 0, 0):
                    self._select_attribute(pos)
                else:
                    cursor.setPosition(pos)
                    self.setTextCursor(cursor)

        self.setTextBackgroundColor(QColor(255, 255, 255))
        self.setTextColor(QColor(0, 0, 0))

        super().keyPressEvent(event)

    def _select_attribute(self, pos):

        text = self.toPlainText()
        text_length = len(text)

        begin, end = pos, pos
        while begin > 0:
            if text[begin] == '{':
                break
            begin -= 1

        while end < text_length:
            if text[end] == '}':
                break
            end += 1

        c = self.textCursor()
        c.setPosition(begin)
        c.setPosition(end + 1, QTextCursor.KeepAnchor)
        self.setTextCursor(c)

    def insert_attribute(self, name):
        self.setTextBackgroundColor(QColor(*self.BACKGROUND_COLOR))
        self.setTextColor(QColor(31, 72, 74))
        self.insertPlainText('{{{}}}'.format(_(name)))
        self.setFocus()


class TemplateEditingWidget(QFrame):

    """
    Single item template.
    """

    def __init__(self, template=None):

        super().__init__()
        return
        self.item = item
        self.template = template

        self.template_text_edit = None
        self.conclusion_text_edit = None

        self._close = self._get_close_func(parent)

        layout = QHBoxLayout()
        self.setLayout(layout)

        layout.addLayout(self._get_text_layout(), stretch=80)
        layout.addWidget(self._get_control_layout(), stretch=20)

    def _get_close_func(self, parent):

        def _close():
            parent.layout.setCurrentIndex(0)

        return _close

    def _get_control_layout(self):
        widget = QWidget()
        vbox = QVBoxLayout()
        widget.setLayout(vbox)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(0)

        scrollable_vbox = QVBoxLayout()
        scrollable_vbox.setContentsMargins(0, 0, 0, 0)
        scrollable_vbox.setSpacing(0)

        for name in self.item.keys():
            b = QPushButton(_(name))
            b.clicked.connect(functools.partial(self.template_text_edit.insert_attribute, name))
            scrollable_vbox.addWidget(b)

        scrollable_vbox = utils.get_scrollable(scrollable_vbox)
        vbox.addWidget(scrollable_vbox)
        vbox.addStretch()

        buttons_layout = QHBoxLayout()
        vbox.addLayout(buttons_layout)

        b = QPushButton('Назад')
        b.clicked.connect(self._close)
        buttons_layout.addWidget(b)

        b = QPushButton('Сохранить')
        b.clicked.connect(self._save)
        buttons_layout.addWidget(b)

        widget.setGraphicsEffect(utils.get_shadow())
        return widget

    def _get_text_layout(self):
        layout = QVBoxLayout()
        self.template_text_edit = TemplateTextEdit()
        self.conclusion_text_edit = QTextEdit()

        self.template_text_edit.setPlaceholderText('Шаблон')
        self.conclusion_text_edit.setPlaceholderText('Заключение')

        self.conclusion_text_edit.setGraphicsEffect(utils.get_shadow())

        layout.addWidget(self.template_text_edit, stretch=80)
        layout.addWidget(self.conclusion_text_edit, stretch=20)
        return layout

    def _save(self, event):
        pass


class TemplateWidget(QFrame):

    """
    Contains menu with the list of items with templates.
    """

    def __init__(self, parent, items):
        super().__init__()

        self.items = items
        self.layout = QStackedLayout()
        self.setLayout(self.layout)
        self.menu_layout = QVBoxLayout()
        self.templates_layout = QStackedLayout()
        self.template_editing_widget = TemplateEditingWidget()

        self.layout.addWidget(self._get_static_widgets())
        self.layout.addWidget(self.template_editing_widget)

    def _get_static_widgets(self):
        hbox = QHBoxLayout()
        hbox.addWidget(utils.get_scrollable(self.menu_layout), stretch=20)
        hbox.addLayout(self.templates_layout, stretch=80)
        hbox.addStretch()
        widget = QWidget()
        widget.setLayout(hbox)
        widget.setGraphicsEffect(utils.get_shadow())
        return widget

    def showEvent(self, event):
        self._show_menu()
        self._show_templates()

    def hideEvent(self, event):
        utils.clear_layout(self.menu_layout)
        utils.clear_layout(self.templates_layout)

    def _show_menu(self):
        for i, item in enumerate(self.items):
            b = QPushButton(_(item.name))
            b.clicked.connect(functools.partial(self.templates_layout.setCurrentIndex, i))
            self.menu_layout.addWidget(b)

    def _show_templates(self):
        cols = 3
        templates = template.Template.get_all()

        for item in self.items:
            grid = QGridLayout()
            for i, each in enumerate(templates[item.id]):
                row, col = i // cols, i % cols
                b = QRadioButton(each.name)
                grid.addWidget(b, row, col)
            self.templates_layout.addWidget(utils.get_scrollable(grid))

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
