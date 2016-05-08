import unidecode
import functools

from PyQt5.Qt import QColor, QKeySequence, Qt, QTextCursor
from PyQt5.QtWidgets import (QFrame, QHBoxLayout, QLabel, QGridLayout,
                             QStackedLayout, QVBoxLayout, QPushButton,
                             QTextEdit, QWidget, QGroupBox, QScrollArea)

from gui import utils


class TemplateTextEdit(QTextEdit):

    BACKGROUND_COLOR = 88, 202, 207

    def __init__(self):

        super().__init__()
        self.setGraphicsEffect(utils.get_shadow())

    def keyPressEvent(self, event):

        pos = self.textCursor().position()
        key = event.key()
        text = self.toPlainText()

        if self.textColor().getRgb()[:-1] != (0, 0, 0):
            if key == Qt.Key_Backspace and pos != 0:
                self._remove_attribute(pos - 1)
            if key == Qt.Key_Delete and pos != len(text):
                self._remove_attribute(pos)

        self.setTextBackgroundColor(QColor(255, 255, 255))
        self.setTextColor(QColor(0, 0, 0))

        super().keyPressEvent(event)

    def _remove_attribute(self, pos):

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


class TemplateWidget(QFrame):

    """
    Single item template.
    """

    def __init__(self, item, template=None):

        super().__init__()

        self.item = item
        self.template = template

        self.template_text_edit = None
        self.conclusion_text_edit = None

        layout = QHBoxLayout()
        self.setLayout(layout)

        layout.addLayout(self._get_text_layout(), stretch=80)
        layout.addWidget(self._get_control_layout(), stretch=20)

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

    def _close(self, event):
        pass

    def _save(self, event):
        pass


class TemplateOptionsWidget(QFrame):

    """
    Contains menu with the list of items with templates.
    """

    def __init__(self, items):
        super().__init__()

        layout = QStackedLayout()
        self.setLayout(layout)
        for item in items:
            layout.addWidget(TemplateWidget(item))


class OptionsWidget(QFrame):

    """
    Widget holds menu with all options.
    """

    def __init__(self, main_window, items, *args):

        super().__init__()

        self.items = items

        layout = QStackedLayout()
        self.setLayout(layout)
        layout.addWidget(self._get_menu_layout())

    def _get_menu_layout(self):

        grid = QGridLayout()
        grid.addWidget(TemplateOptionsWidget(self.items), 0, 0)

        widget = QWidget()
        widget.setLayout(grid)
        return widget
