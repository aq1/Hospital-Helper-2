from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel, QFormLayout, QLineEdit, QPushButton


class CrudWidget(QFrame):

    def __init__(self, main_window, base, db_object):
        super().__init__(main_window)
        self.setFixedSize(main_window.size())
        c = CrudWidgetContent(self, base, db_object)


class CrudWidgetContent(QFrame):

    def __init__(self, parent, base, db_object=None):

        super().__init__(parent)

        layout = QFormLayout()
        self.setLayout(layout)
        for col in base.__table__.columns:
            layout.addRow(col.name, QLineEdit())
        layout.addRow(QPushButton('3'), QPushButton('3'))