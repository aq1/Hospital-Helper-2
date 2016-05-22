import os
import sys
import functools

from PyQt5 import QtCore
from PyQt5.QtCore import QCoreApplication, Qt, QObject, pyqtSignal
from PyQt5.QtWidgets import (QWidget, QStackedLayout, QDesktopWidget,
                             QVBoxLayout, QShortcut, QApplication, QSplashScreen)

from PyQt5.QtGui import QKeySequence, QPixmap

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


class Communication(QObject):

    toggle_select_item = pyqtSignal()
    resized = pyqtSignal(float, float)
    set_select_item_visibility = pyqtSignal(bool)
    ctrl_hotkey = pyqtSignal(bool)
    menu_button_clicked = pyqtSignal(int)
    user_selected = pyqtSignal(object)
    item_selected = pyqtSignal(int)
    menu_item_selected = pyqtSignal(int)
    input_changed_signal = pyqtSignal(str)


class MainWindow(QWidget):

    MENU_LABELS = [each['sys'] for each in options.CONTROL_BUTTONS_LABELS]

    def __init__(self, items):
        super().__init__()

        self.items = items
        self.user = None

        self.communication = Communication()
        self.communication.menu_item_selected.connect(self.menu_item_selected)

        self._set_sys_attributes()

        # self.action_button = ActionButton(self)
        self.stacked_layout = QStackedLayout()
        # Order matters
        frames = [
            DataWidget(self, self.items),
            TemplateWidget(self, self.items, widget_for_select=True),
            DBWidget(self),
            OptionsWidget(self, self.items),
            UsersWidget(self),
        ]

        for i, frame in enumerate(frames):
            if isinstance(frame, DataWidget):
                self.data_frame_index = i
            self.stacked_layout.addWidget(frame)

        self.stacked_layout.setCurrentIndex(len(frames) - 1)
        vbox = QVBoxLayout()
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(0)
        self.setLayout(vbox)

        top_frame = TopFrame(self, items)
        vbox.addWidget(top_frame, stretch=15)
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

    def user_selected(self, user):
        self.user = user
        self.communication.user_selected.emit(user)
        self._set_shortcuts()
        self.stacked_layout.setCurrentIndex(0)

    def menu_item_selected(self, index):
        if self.stacked_layout.currentIndex() == index == self.data_frame_index:
            self.communication.toggle_select_item.emit()
            return
        else:
            self.communication.set_select_item_visibility.emit(False)
        self.stacked_layout.setCurrentIndex(index)

        # try:
        #     icon = self.frames[index].ACTION_BTN_ICON
        #     func = self.frames[index].action_btn_function
        # except AttributeError:
        #     self.action_button.hide()
        # else:
        #     self.action_button.toggle_state(icon, func)
        #     self.action_button.show()
        #     self.action_button.raise_()

    def input_changed(self, item):
        # Well it doesnt look good, but i was never good with UI.
        if self.items.index(item) == 0:
            text = []
            for i, key in enumerate(item.keys()):
                if item[key]:
                    text.append(str(item[key]))

                if i == 2:
                    break

            self.communication.input_changed_signal.emit(' '.join(text))

        # self.top_sys_btns.set_title('{} {}. {}.'.format(user.surname, user.name[0], user.patronymic[0]))

    # def _shortcut_pressed(self, key_code):
    #     try:
    #         return
    #         # self.select_item(self.select_menu.get_item_index_by_key(key_code))
    #     except (IndexError, TypeError):
    #         pass

    def keyPressEvent(self, event):
        mods = event.modifiers()
        if mods & QtCore.Qt.ControlModifier:
            if event.text() is '':
                self.communication.ctrl_hotkey.emit(True)
            elif event.key() == Qt.Key_Return and self.stacked_layout.currentIndex() == 0:
                pass

    def keyReleaseEvent(self, event):
        if (event.text() is ''):
            self.communication.ctrl_hotkey.emit(False)

    def _set_shortcuts(self):
        QShortcut(QKeySequence('Esc'), self).activated.connect(self.close)
        # for key, key_code in self.select_menu.HINTS:
        #     QShortcut(QKeySequence('Ctrl+{}'.format(key)), self).activated.connect(
        #         functools.partial(self._shortcut_pressed, key_code))

    def top_frame_resized(self, frame, event):
        waterline = frame.y() + frame.height()
        self.communication.resized.emit(self.width(), waterline)

    def create_crud_widget(self, base, callback=None, db_object=None):
        CrudWidget(self, base, callback, db_object)

    def close(self, event=None):
        QCoreApplication.instance().quit()

    def minimize(self, event=None):
        self.setWindowState(Qt.WindowMinimized)


def init(items):
    app = QApplication(sys.argv)
    # splash_img = QPixmap(os.path.join(options.STATIC_DIR, 'splash.png'))
    # splash = QSplashScreen(splash_img)
    # splash.show()

    style = []
    style_dir = os.path.join(options.STATIC_DIR, 'style')
    for f in os.listdir(style_dir):
        if not f.endswith('.qss'):
            continue
        with open(os.path.join(style_dir, f), 'r') as qss:
            style.append(qss.read())
    app.setStyleSheet('\n'.join(style))

    mw = MainWindow(items)
    # splash.finish(mw)

    sys.exit(app.exec_())
