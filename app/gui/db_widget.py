from PyQt5.QtWidgets import QWidget, QFrame, QHBoxLayout, QLabel, QGridLayout

from model import db


class DBWidget(QFrame):

    ACTION_BTN_ICON = 'plus'
    ITEMS_PER_PAGE = 100

    def __init__(self, main_window):

        super().__init__()

        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.columns = []

        self.display_model(db.Client)

    def display_model(self, model):
        self._clear_layout()

        items = db.SESSION.query(model)
        print(items)
        self.columns = []
        for j, c in enumerate(model.__table__.columns):
            self.columns.append(c.name)
            self.layout.addWidget(QLabel(_(c.name)), 0, j)

        for i, item in enumerate(items, 1):
            self._add_row(i, item)

    def _clear_layout(self):
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().deleteLater()

    def _add_row(self, row_id, item):
        for j, c in enumerate(self.columns):
            self.layout.addWidget(QLabel(getattr(item, c)), row_id, j)

    def action_btn_function(self):
        print('db')
