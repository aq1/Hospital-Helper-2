import functools

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import (QWidget, QFrame, QLabel, QHBoxLayout,
                             QVBoxLayout, QPushButton, QGraphicsDropShadowEffect,
                             QLineEdit, QFormLayout, QStackedLayout)


class ReportTypeSelectWidget(QWidget):

    def __init__(self, parent, item, templates):
        super().__init__()

        self.templates = templates
        self.item = item

        vbox = QVBoxLayout()
        self.setLayout(vbox)
        vbox.setSpacing(0)
        vbox.setContentsMargins(0, 0, 0, 0)
        # self.setMaximumHeight(400)

        l = QLabel(_(item.name))
        # l.setAlignment(Qt.AlignCenter)
        vbox.addWidget(l)
        for templ in templates:
            b = QPushButton(_(templ.name))
            vbox.addWidget(b)

        vbox.addStretch()

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        self.setGraphicsEffect(shadow)


class ReportWidget(QFrame):

    SELECTED_BTN_STYLE = 'background-color: #58CACF; color: white;'
    LEFT_MARGIN = 25

    def __init__(self, main_window, items, templates):

        super().__init__()

        self.main_window = main_window
        self.reportWidgets = []
        self.templates = templates
        self.setMinimumSize(main_window.width() * 2.5, main_window.height())
        self.timer = QTimer(self)
        self.scroll_value = 0
        self.scroll_direction = 0

        hbox = QHBoxLayout()
        self.setLayout(hbox)
        hbox.addSpacing(self.LEFT_MARGIN)
        hbox.setSpacing(0)
        hbox.setContentsMargins(0, 0, 0, 0)

        for item in items:
            r = ReportTypeSelectWidget(self, item, templates[item.id])
            r.hide()
            self.reportWidgets.append(r)
            hbox.addWidget(r)
            hbox.addSpacing(15)
        hbox.addStretch()

        self.timer.timeout.connect(functools.partial(self.timer_event))
        self.timer.setInterval(10)

    def timer_event(self):
        if not self.scroll_direction or self.scroll_value <= 0:
            return

        self.scroll_value -= 1
        self._scroll()

    def _scroll(self):

        if not (self.scroll_value and self.scroll_direction):
            return

        widgets = self.findChildren(ReportTypeSelectWidget)

        if self.scroll_direction > 0 and widgets[0].x() >= self.LEFT_MARGIN:
            return
        if self.scroll_direction < 0 and widgets[-1].x() + widgets[-1].width() <= self.main_window.width() - self.LEFT_MARGIN:
            return

        for each in widgets:
            each.move(each.x() + self.scroll_direction * self.scroll_value, each.y())

    def wheelEvent(self, event):
        self.scroll_value = 30
        if event.angleDelta().y() > 0:
            self.scroll_direction = 1
        else:
            self.scroll_direction = -1

    def hideEvent(self, event):
        self.timer.stop()

    def showEvent(self, event):
        self.timer.start()

        for widget in self.reportWidgets:
            widget.hide()
            for value in widget.item.values():
                if value:
                    widget.show()
                    print(value)
                    break
        # self._show_templates_widgets()
