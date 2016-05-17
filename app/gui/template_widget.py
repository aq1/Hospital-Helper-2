import functools

from PyQt5.Qt import QColor, Qt, QTextCursor
from PyQt5.QtWidgets import (QFrame, QHBoxLayout, QLabel, QGridLayout,
                             QStackedLayout, QVBoxLayout, QPushButton,
                             QTextEdit, QWidget, QGroupBox, QScrollArea,
                             QRadioButton, QLineEdit)

from model import template as template_module

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
    Widget for editing the tempate.
    """

    def __init__(self, close_func):

        super().__init__()

        self.name_text_edit = None
        self.template_text_edit = None
        self.conclusion_text_edit = None
        self.controls_layout = QVBoxLayout()
        self._close = close_func

        layout = QHBoxLayout()
        self.setLayout(layout)

        layout.addLayout(self._get_text_layout(), stretch=80)
        layout.addWidget(self._get_control_layout(), stretch=20)

    def _get_control_layout(self):
        widget = QWidget()
        vbox = QVBoxLayout()
        widget.setLayout(vbox)
        vbox.setContentsMargins(0, 0, 0, 0)
        # vbox.setSpacing(0)

        scrollable_vbox = utils.get_scrollable(self.controls_layout)
        vbox.addWidget(scrollable_vbox, stretch=80)
        # vbox.addSpacing(20)

        buttons_layout = QHBoxLayout()
        vbox.addLayout(buttons_layout, stretch=20)

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
        self.name_text_edit = QLineEdit()

        for w, p, s in zip(self._get_all_text_fields(),
                           ('Имя', 'Шаблон', 'Заключение'),
                           (5, 80, 15)):
            w.setPlaceholderText(p)
            w.setGraphicsEffect(utils.get_shadow())
            layout.addWidget(w, stretch=s)

        return layout

    def _get_all_text_fields(self):
        return self.name_text_edit, self.template_text_edit, self.conclusion_text_edit

    def _show(self, item, template=None):
        for name in item.keys():
            b = QPushButton(_(name))
            b.clicked.connect(functools.partial(self.template_text_edit.insert_attribute, name))
            self.controls_layout.addWidget(b)

        if not template:
            return

        for w, t in zip(self._get_all_text_fields(),
                        (template.name, template.body, template.conclusion)):
            w.setText(t)

    def hideEvent(self, event):
        for w in (self._get_all_text_fields()):
            w.setText('')
        utils.clear_layout(self.controls_layout)

    def _save(self, event):
        pass


class TemplateWidget(QFrame):

    """
    Contains menu with the list of items with templates.
    """

    def __init__(self, main_window, items, widget_for_select):
        super().__init__()

        self.main_window = main_window
        self.items = items
        self.visible_items = []
        self.widget_for_select = widget_for_select
        self.layout = QStackedLayout()
        self.menu_layout = QVBoxLayout()
        self.templates_layout = QStackedLayout()
        self.template_editing_widget = TemplateEditingWidget(lambda: self.layout.setCurrentIndex(0))
        self.ACTION_BTN_ICON = ['plus', 'check'][widget_for_select]
        self._template_clicked = [self._template_selected_for_editing,
                                  self._template_selected_for_report][widget_for_select]

        self.setLayout(self.layout)

        self.layout.addWidget(self._get_static_widgets())
        self.layout.addWidget(self.template_editing_widget)

    def _get_static_widgets(self):
        hbox = QHBoxLayout()
        hbox.addWidget(utils.get_scrollable(self.menu_layout), stretch=30)
        hbox.addLayout(self.templates_layout, stretch=70)
        # hbox.addStretch(10)
        widget = QWidget()
        widget.setLayout(hbox)
        widget.setGraphicsEffect(utils.get_shadow())
        return widget

    def _iterate_items(self):
        if not self.widget_for_select:
            return self.items

        items = []
        for item in self.items:
            for value in item.values():
                if value:
                    items.append(item)
                    break

        return items

    def showEvent(self, event):
        self.visible_items = self._iterate_items()
        self.main_window.action_button.show()
        self._show_menu()
        self._show_templates()

    def hideEvent(self, event):
        utils.clear_layout(self.menu_layout)
        utils.clear_layout(self.templates_layout)
        self.layout.setCurrentIndex(0)

    def _show_menu(self):
        items = self.visible_items
        for i, item in enumerate(items):
            b = QRadioButton(self._get_button_name(item))
            b.setChecked(i == 0)
            b.clicked.connect(functools.partial(self.templates_layout.setCurrentIndex, i))
            b.setObjectName('menu_button')
            self.menu_layout.addWidget(b)

        if not items:
            self.menu_layout.addStretch()
            l = QLabel('Чтобы создать отчет\nначните заполнять данные')
            l.setAlignment(Qt.AlignCenter)
            self.menu_layout.addWidget(l)

        self.menu_layout.addStretch()

    def _show_templates(self):
        cols = 3
        templates = template_module.Template.get_all()

        for j, item in enumerate(self.visible_items):
            grid = QGridLayout()
            for i, each in enumerate(templates[item.id]):
                row, col = i // cols, i % cols
                b = QRadioButton(each.name)
                b.setChecked(item.template == each)
                b.clicked.connect(functools.partial(self._template_clicked, j, each))
                grid.addWidget(b, row, col)
            self.templates_layout.addWidget(utils.get_scrollable(grid))

    def _template_selected_for_report(self, index, template):
        self.visible_items[index].template = template
        buttons = self.findChildren(QRadioButton, name='menu_button')
        buttons[index].setText(self._get_button_name(self.visible_items[index]))
        for i in range(len(self.visible_items)):
            ind = (i + index) % len(self.visible_items)
            if not self.visible_items[ind].template:
                self.templates_layout.setCurrentIndex(ind)
                buttons[ind].setChecked(True)
                buttons[index].setChecked(False)
                return

    def _template_selected_for_editing(self, index, template=None):
        self.layout.setCurrentIndex(1)
        self.main_window.action_button.hide()
        self.template_editing_widget._show(self.items[index], template)

    def _get_button_name(self, item):

        if item.template:
            return '{} - {}'.format(_(item.name), item.template.name)
        else:
            return _(item.name)

    def action_btn_function(self):
        pass
