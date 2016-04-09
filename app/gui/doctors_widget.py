import functools

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QFrame, QGroupBox, QVBoxLayout, QLabel,
                             QScrollArea, QRadioButton, QGraphicsDropShadowEffect,
                             QHBoxLayout, QPushButton)

from model import db


class DoctorsWidget(QFrame):

    ACTION_BTN_ICON = 'check'

    def __init__(self, main_window):

        super().__init__()

        self.main_window = main_window

        groupbox = QGroupBox()

        vbox = QVBoxLayout()
        vbox.setSpacing(0)
        vbox.setContentsMargins(0, 0, 0, 0)

        self.doctors = db.SESSION.query(db.Doctor).all()
        hospitals = db.SESSION.query(db.Hospital).all()

        for hospital in hospitals:
            l = QLabel(hospital.name)
            l.setAlignment(Qt.AlignCenter)
            vbox.addWidget(l)
            for doctor in self.doctors:
                if doctor.hospital_id == hospital.id:
                    fullname = '{} {} {}'.format(doctor.surname, doctor.name, doctor.patronymic)
                    b = QRadioButton(fullname)
                    b.mouseDoubleClickEvent = (functools.partial(self._button_clicked, doctor))
                    vbox.addWidget(b)

        vbox.addStretch()

        b = QPushButton('Добавить')
        b.clicked.connect(functools.partial(main_window.create_crud_widget, db.Doctor, self.doctor_created))
        vbox.addWidget(b)

        groupbox.setLayout(vbox)
        scroll = QScrollArea()
        scroll.setWidget(groupbox)
        scroll.setWidgetResizable(True)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        this_vbox = QHBoxLayout(self)
        this_vbox.addStretch(25)
        this_vbox.addWidget(scroll, stretch=50)
        this_vbox.addStretch(25)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        self.setGraphicsEffect(shadow)

    def _button_clicked(self, doctor, event):
        self.main_window.doctor_selected(doctor)

    def action_btn_function(self):
        for i, b in enumerate(self.findChildren(QRadioButton)):
            if b.isChecked():
                self.main_window.doctor_selected(self.doctors[i])

    def doctor_created(self, doctor):
        print('hey')
