import functools

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QFrame, QGroupBox, QVBoxLayout, QLabel,
                             QScrollArea, QRadioButton, QGraphicsDropShadowEffect,
                             QHBoxLayout)

from model import db


class DoctorsWidget(QFrame):

    def __init__(self, main_window):

        super().__init__()

        self.main_window = main_window

        groupbox = QGroupBox()

        vbox = QVBoxLayout()
        vbox.setSpacing(0)
        vbox.setContentsMargins(0, 0, 0, 0)

        doctors = db.SESSION.query(db.Doctor).all()
        hospitals = db.SESSION.query(db.Hospital).all()

        for hospital in hospitals:
            vbox.addWidget(QLabel(hospital.name))
            for doctor in doctors:
                if doctor.hospital_id == hospital.id:
                    fullname = '{} {}. {}.'.format(doctor.surname, doctor.name[0], doctor.patronymic[0])
                    b = QRadioButton(fullname)
                    b.clicked.connect(functools.partial(self._button_clicked, doctor))
                    vbox.addWidget(b)

        vbox.addStretch()

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

    def _button_clicked(self, doctor):
        self.main_window.doctor_selected(doctor)
