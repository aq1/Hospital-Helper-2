from PyQt5.QtWidgets import (
    QWidget, QFrame, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QGraphicsDropShadowEffect)


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

        vbox = QVBoxLayout()
        vbox.widgetResizable = True
        vbox.addSpacing(main_window.TOP_MARGIN)
        vbox.setSpacing(0)
        vbox.setContentsMargins(0, 0, 0, 0)
        self.list_wrapper = QWidget()
        self.list_wrapper.wheelEvent = self.item_list_scroll
        self.list_wrapper.setLayout(vbox)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        self.list_wrapper.setGraphicsEffect(shadow)

        self.buttons = []
        for item in items:
            b = QPushButton(_(item.name))
            b.clicked.connect(self.button_clicked)
            self.buttons.append(b)
            vbox.addWidget(b)

        hbox.addSpacing(25)
        hbox.addWidget(self.list_wrapper, stretch=10)
        vbox = QVBoxLayout()
        vbox.setSpacing(0)
        vbox.setContentsMargins(0, 0, 0, 0)
        hbox.addLayout(vbox, stretch=40)

        hbox.addStretch()

    def button_clicked(self, event):
        self.move(0, 100)
        # self.lower()

    def item_list_scroll(self, event):

        self.lower()

        if event.angleDelta().y() > 0:
            b = self.buttons[-1]
            if self.mapTo(self.main_window, b.pos()).y() + b.height() <= self.main_window.height() - self.main_window.TOP_MARGIN:
                return
            delta = -10
        else:
            b = self.buttons[0]
            if self.mapTo(self, b.pos()).y() >= self.main_window.TOP_MARGIN:
                return
            delta = 10

        for each in self.buttons:
            each.move(each.x(), each.y() + delta)
