from PyQt5.QtWidgets import QFrame, QLabel, QHBoxLayout


class ReportWidget(QFrame):

    def __init__(self, main_window, items):

        super().__init__()
        hbox = QHBoxLayout()
        self.setLayout(hbox)
        hbox.addWidget(QLabel('Report widget'))
