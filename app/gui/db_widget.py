from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel


class DBWidget(QFrame):

    ACTION_BTN_ICON = 'plus'

    def __init__(self, main_window, db):

        super().__init__()
        hbox = QHBoxLayout()
        self.setLayout(hbox)
        hbox.addWidget(QLabel('DB widget'))

    def action_btn_function(self):
        print('db')
