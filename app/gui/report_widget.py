from PyQt5.QtWidgets import (
    QWidget, QFrame, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QGraphicsDropShadowEffect, QLineEdit)


class ReportWidget(QWidget):

    def __init__(self, main_window, items, templates):

        super().__init__()

        self.main_window = main_window
        self.templates = templates
        self.setFixedSize(self.main_window.width(), self.main_window.height())

        hbox = QHBoxLayout()
        self.setLayout(hbox)
        hbox.setSpacing(0)
        hbox.setContentsMargins(0, 0, 0, 0)

        self.select_wrapper = QFrame()
        hbox.addWidget(self.select_wrapper)
        hbox.addStretch()
        # self.select_wrapper.wheelEvent = self.scroll_event
        wrapper_layout = QVBoxLayout()
        self.select_wrapper.setLayout(wrapper_layout)

        wrapper_layout.addSpacing(main_window.TOP_MARGIN)
        wrapper_layout.setSpacing(0)
        wrapper_layout.setContentsMargins(0, 0, 0, 0)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        # self.select_wrapper.setGraphicsEffect(shadow)

        for item in items:
            hb = QHBoxLayout()
            wrapper_layout.addLayout(hb)
            hb.addWidget(QLabel(_(item.name)))
            hb.addWidget(QLineEdit())

    def _scroll(self, value):
        self.select_wrapper.move(self.select_wrapper.x(), self.select_wrapper.y() + value)

    def wheelEvent(self, event):
        w = self.select_wrapper
        self.lower()
        if event.angleDelta().y() > 0:
            if w.y() > 0:
                return
            # if self.mapTo(self, w.pos()).y() <= self.y() + self.main_window.TOP_MARGIN:
                # return
            self._scroll(20)
        else:
            if self.mapTo(self.main_window, w.pos()).y() + w.height() <= self.main_window.height():
                return
            self._scroll(-20)


    #     self.buttons = []
    #     for item in items:
    #         hb = QHBoxLayout()
    #         hb.addWidget(QLabel(_(item.name)))
    #         hb.addWidget(QLineEdit())
    #         self.buttons.append(hb)
    #         vbox.addLayout(hb)

    #     hbox.addSpacing(25)
    #     hbox.addWidget(self.list_wrapper, stretch=10)
    #     vbox = QVBoxLayout()
    #     vbox.setSpacing(0)
    #     vbox.setContentsMargins(0, 0, 0, 0)
    #     hbox.addLayout(vbox, stretch=40)

    #     hbox.addStretch()

    # def button_clicked(self, event):
    #     pass
    #     # self.move(0, 100)
    #     # self.lower()

    # def item_list_scroll(self, event):


    #     if event.angleDelta().y() > 0:
    #         b = self.buttons[-1]
    #         if self.mapTo(self.main_window, b.pos()).y() + b.height() <= self.main_window.height() - self.main_window.TOP_MARGIN:
    #             return
    #         delta = -10
    #     else:
    #         b = self.buttons[0]
    #         if self.mapTo(self, b.pos()).y() >= self.main_window.TOP_MARGIN:
    #             return
    #         delta = 10

    #     for each in self.buttons:
    #         each.move(each.x(), each.y() + delta)
