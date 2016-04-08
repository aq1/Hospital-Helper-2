from PyQt5.QtWidgets import QFrame, QFormLayout, QLineEdit, QPushButton, QComboBox, QLabel

# from sqlalchemy import (Column, Integer, String, Float, ForeignKey, Date, SmallInteger, Text)


from model import db


class CrudWidget(QFrame):

    def __init__(self, main_window, base, db_object):
        super().__init__(main_window)
        self.setFixedSize(main_window.size())
        self.show()
        self.mw = main_window
        self.move(0, main_window.top_sys_btns.height())
        self.raise_()
        CrudWidgetContent(self, base, db_object)


class CrudWidgetContent(QFrame):

    def __init__(self, parent, base, db_object=None):

        super().__init__(parent)
        layout = QFormLayout()
        self.setLayout(layout)
        for col in base.__table__.columns:
            # self._get_row(col)
            layout.addRow(*self._get_row(col))
        layout.addRow(QPushButton('3'), QPushButton('3'))
        self.p = parent
        self.show()
        self.raise_()
        self.move((parent.width() - self.width()) / 2, (parent.height() - self.height()) / 2)

    def _get_row(self, column):
        """
        Default row for a form is QLabel, QLineEdit
        But for foreign fields it's QComboBox
        Maybe later I will add QCalendar for dates and etc.
        """

        if not column.foreign_keys:
            return QLabel(_(column.name)), QLineEdit()

        label = column.name
        if label.endswith('_id'):
            label = column.name[:-3]

#       self.hospital = db.SESSION.query(db.Hospital).get(self.doctor.hospital_id)

        table = db.Base.metadata.tables.get(column.foreign_keys)
        options = db.SESSION.query()
        #     return QLabel(_(column.name)), QComboBox()
        # else:
