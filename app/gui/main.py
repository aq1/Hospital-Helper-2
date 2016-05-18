import os
import sys
import functools

from PyQt5 import QtCore
from PyQt5.QtCore import QCoreApplication, Qt, QObject, pyqtSignal
from PyQt5.QtWidgets import (QWidget, QStackedLayout, QDesktopWidget,
                             QVBoxLayout, QShortcut, QApplication)

from PyQt5.QtGui import QKeySequence

import options

from gui.users_widget import UsersWidget
from gui.select_menu import SelectMenu, SelectItemMenu
from gui.data_widget import DataWidget
from gui.db_widget import DBWidget
from gui.options_widget import OptionsWidget
from gui.template_widget import TemplateWidget
from gui.top_frame import TopFrame
from gui.action_button import ActionButton
from gui.crud_widget import CrudWidget


class ActionsMixin:

    # def _set_shortcuts(self):
    #     QShortcut(QKeySequence('Esc'), self).activated.connect(self.close)

    #     # for key, key_code in self.select_menu.HINTS:
    #     #     QShortcut(QKeySequence('Ctrl+{}'.format(key)), self).activated.connect(
    #     #         functools.partial(self._shortcut_pressed, key_code))

    def top_frame_resized(self, frame, event):
        waterline = frame.y() + frame.height()
        self.communication.resized.emit(self.width(), waterline)

    # def set_select_menu_item_visibility(self, value, event=None):
    #     # Event is triggered only on 'Data' tab
    #     if not self.stacked_layout.currentIndex():
    #         return
    #         # self.select_menu.setVisible(value)
    #         # self.select_menu.raise_()

    # def data_button_entered(self, event):
    #     # Event is triggered only on 'Data' tab
    #     if not self.stack_index:
    #         self.set_select_menu_item_visibility(True)

    def select_menu_button_clicked(self, index):
        if self.stacked_layout.currentIndex() == index == 0:
            self.communication.toggle_select_item.emit()
        else:
            self.communication.set_select_item_visibility.emit(False)
        self.stacked_layout.setCurrentIndex(index)

        try:
            icon = self.frames[index].ACTION_BTN_ICON
            func = self.frames[index].action_btn_function
        except AttributeError:
            self.action_button.hide()
        else:
            self.action_button.toggle_state(icon, func)
            self.action_button.show()
            self.action_button.raise_()

    # def input_changed(self, item):
    #     # Well it doesnt look good, but i was never good with UI.
    #     if self.items.index(item) == 0:
    #         text = []
    #         for i, key in enumerate(item.keys()):
    #             if item[key]:
    #                 text.append(str(item[key]))

    #             if i == 2:
    #                 break

    #         self.findChild(TopFrame).set_label_text(' '.join(text))

    # def user_selected(self, user):
    #     # self.select_menu_button_clicked(0)
    #     self.user = user
    #     self.findChild(SelectMenu).show()
    #     self._set_shortcuts()
    #     # self.top_sys_btns.set_title('{} {}. {}.'.format(user.surname, user.name[0], user.patronymic[0]))

    # def _shortcut_pressed(self, key_code):
    #     try:
    #         return
    #         # self.select_item(self.select_menu.get_item_index_by_key(key_code))
    #     except (IndexError, TypeError):
    #         pass

    # def keyPressEvent(self, event):
    #     mods = event.modifiers()
    #     if mods & QtCore.Qt.ControlModifier:
    #         if event.text() is '':
    #             self.set_select_menu_item_visibility(True)
    #             # self.select_menu.toggle_hints(True)
    #         elif event.key() == Qt.Key_Return and self.stacked_layout.currentIndex() == 0:
    #             self.findChild(SelectMenu).button_clicked(1)

    # def keyReleaseEvent(self, event):
    #     if (event.text() is ''):
    #         self.set_select_menu_item_visibility(False)
    #         # self.select_menu.toggle_hints(False)

    def create_crud_widget(self, base, callback=None, db_object=None):
        cw = CrudWidget(self, base, callback, db_object)

    def close(self, event=None):
        QCoreApplication.instance().quit()

    def minimize(self, event=None):
        self.setWindowState(Qt.WindowMinimized)


class Communication(QObject):

    toggle_select_item = pyqtSignal()
    resized = pyqtSignal(float, float)
    set_select_item_visibility = pyqtSignal(bool)
    menu_button_clicked = pyqtSignal(int)
    user_selected = pyqtSignal(object)
    item_selected = pyqtSignal(int)


class MainWindow(QWidget, ActionsMixin):

    MENU_LABELS = [each['sys'] for each in options.CONTROL_BUTTONS_LABELS]
    TOP_MARGIN = 50

    def __init__(self, items):
        super().__init__()

        self.items = items
        self.user = None
        self.communication = Communication()

        self._set_sys_attributes()

        self.action_button = ActionButton(self)
        self.stacked_layout = QStackedLayout()
        # Order matters
        frames = [DataWidget(self, self.items),
                  TemplateWidget(self, self.items, widget_for_select=True),
                  DBWidget(self),
                  OptionsWidget(self, self.items),
                  UsersWidget(self)]

        for frame in frames:
            self.stacked_layout.addWidget(frame)

        vbox = QVBoxLayout()
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(0)
        self.setLayout(vbox)

        top_frame = TopFrame(self, items)
        vbox.addWidget(top_frame, stretch=15)
        vbox.addSpacing(self.TOP_MARGIN)
        vbox.addLayout(self.stacked_layout, stretch=40)
        self.show()

    def _set_sys_attributes(self):
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setWindowTitle('Hospital Helper')
        dw = QDesktopWidget()
        w = dw.geometry().size().width() * 0.75
        self.setFixedSize(w, w * 0.6)
        qr = self.frameGeometry()
        cp = dw.availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


def init(items):
    app = QApplication(sys.argv)

    style = []
    style_dir = os.path.join(options.STATIC_DIR, 'style')
    for f in os.listdir(style_dir):
        if not f.endswith('.qss'):
            continue
        with open(os.path.join(style_dir, f), 'r') as qss:
            style.append(qss.read())
    app.setStyleSheet('\n'.join(style))

    mw = MainWindow(items)
    sys.exit(app.exec_())
