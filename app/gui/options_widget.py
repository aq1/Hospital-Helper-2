import unidecode
import functools

from PyQt5.Qt import QColor
from PyQt5.QtWidgets import (QFrame, QHBoxLayout, QLabel, QGridLayout,
                             QStackedLayout, QVBoxLayout, QPushButton,
                             QTextEdit, QWidget)


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

        layout.addLayout(self._get_text_layout())
        layout.addLayout(self._get_control_layout())

    def _get_control_layout(self):
        vbox = QVBoxLayout()
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(0)

        for name in self.item.keys():
            b = QPushButton(name)
            b.clicked.connect(functools.partial(self._add_attribute, name))
            vbox.addWidget(b)
        vbox.addStretch()

        buttons_layout = QHBoxLayout()
        vbox.addLayout(buttons_layout)

        b = QPushButton('Назад')
        b.clicked.connect(self._close)
        buttons_layout.addWidget(b)

        b = QPushButton('Сохранить')
        b.clicked.connect(self._save)
        buttons_layout.addWidget(b)

        return vbox

    def _get_text_layout(self):
        layout = QVBoxLayout()
        self.template_text_edit = QTextEdit()
        self.conclusion_text_edit = QTextEdit()

        self.template_text_edit.setPlaceholderText('Шаблон')
        self.conclusion_text_edit.setPlaceholderText('Заключение')

        self.template_text_edit.textChanged.connect(self._f)

        layout.addWidget(self.template_text_edit, stretch=80)
        layout.addWidget(self.conclusion_text_edit, stretch=20)
        return layout

    def _f(self):
        self.template_text_edit.setTextBackgroundColor(QColor(255, 255, 255))
        self.template_text_edit.setTextColor(QColor(0, 0, 0))

    def _add_attribute(self, name):
        self.template_text_edit.setTextBackgroundColor(QColor(31, 72, 74))
        self.template_text_edit.setTextColor(QColor(255, 255, 255))
        self.template_text_edit.insertPlainText('{{{}}}'.format(_(name)))
        self.template_text_edit.setFocus()
        # self.template_text_edit.insertHtml('<span style="color: red">{{{}}}</span>'.format(_(name)))

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
