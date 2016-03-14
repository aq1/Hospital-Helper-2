from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel


class OptionsWidget(QFrame):

    def __init__(self, main_window, *args):

        super().__init__()
        hbox = QHBoxLayout()
        self.setLayout(hbox)
        hbox.addWidget(QLabel('Options widget'))
