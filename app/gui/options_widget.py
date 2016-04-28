from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel, QGridLayout


class OptionsWidget(QFrame):

    def __init__(self, main_window, *args):

        super().__init__()
        layout = QGridLayout()
        self.setLayout(layout)
