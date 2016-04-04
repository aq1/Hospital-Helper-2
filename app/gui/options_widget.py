from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel


class OptionsWidget(QFrame):

    ACTION_BTN_ICON = None

    def __init__(self, main_window, *args):

        super().__init__()
        hbox = QHBoxLayout()
        self.setLayout(hbox)
        hbox.addWidget(QLabel('Options widget'))

    def action_btn_function(self):
        print('options')
