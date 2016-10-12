import os
import functools

from PyQt5.Qt import QFont
from PyQt5.QtGui import QTextCharFormat, QIcon
from PyQt5.QtWidgets import (QFrame, QHBoxLayout, QVBoxLayout, QPushButton, QTextEdit)

from app import options
from app.gui import utils


class TextControls(QFrame):

    """
    Group of buttons for text format.
    """

    def __init__(self, text_edit):
        super().__init__()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        for n in 'b', 'i', 'u', 'la', 'ca', 'ra':
            b = QPushButton()
            b.setIcon(QIcon(os.path.join(options.STATIC_DIR, 'icons', n + '.png')))
            b.clicked.connect(functools.partial(text_edit.format_selected, n))
            layout.addWidget(b)

        layout.addStretch()
        self.setGraphicsEffect(utils.get_shadow())


class TemplateTextEdit(QTextEdit):

    """
    Custom widget with syntax highlighting and custom controls.
    """

    def __init__(self, highlighter=None):

        super().__init__()
        self.setGraphicsEffect(utils.get_shadow())
        if highlighter:
            self.highlighter = highlighter
        self.keywords = []

    def insert_attribute(self, item, name):
        self.insertPlainText('{{{i}.{n}}}'.format(i=_(item.name), n=_(name)))
        self.setFocus()

    def set_rules(self, item):
        if self.highlighter:
            self.highlighter.set_rules(item)

    def _get_bold(self):
        _format = QTextCharFormat()
        if self.textCursor().charFormat().font().bold():
            _format.setFontWeight(QFont.Normal)
        else:
            _format.setFontWeight(QFont.Bold)

        return _format

    def _get_cursive(self):
        _format = QTextCharFormat()
        if self.textCursor().charFormat().font().italic():
            _format.setFontItalic(False)
        else:
            _format.setFontItalic(True)

        return _format

    def _get_underline(self):
        _format = QTextCharFormat()
        if self.textCursor().charFormat().font().underline():
            _format.setFontUnderline(False)
        else:
            _format.setFontUnderline(True)

        return _format

    def _get_format(self, f):
        return {
            'b': self._get_bold,
            'i': self._get_cursive,
            'u': self._get_underline
        }[f]()

    def format_selected(self, f):
        self.textCursor().mergeCharFormat(self._get_format(f))


class TextEditWithFormatControls(QFrame):

    def __init__(self, highlighter=None):
        super().__init__()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.template_text_edit = TemplateTextEdit(highlighter)
        self.text_controls = TextControls(self.template_text_edit)
        layout.addWidget(self.text_controls)
        layout.addWidget(self.template_text_edit)

    def __getattr__(self, a):
        return getattr(self.template_text_edit, a)
