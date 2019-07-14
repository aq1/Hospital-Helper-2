import os
import csv
import datetime
import functools
import subprocess

from odf import text, teletype
from odf.opendocument import load
from sqlalchemy import extract

from PyQt5.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QLineEdit,
)

from app.model import db
from app import options


class JournalWidget(QFrame):

    def __init__(self, main_window, parent):
        super().__init__()

        self._create_layout(main_window, parent)

    def _create_layout(self, main_window, parent):
        layout = QHBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(20)

        vbox = QVBoxLayout()
        vbox.setContentsMargins(15, 15, 15, 15)
        vbox.setSpacing(20)

        year_input = QLineEdit()
        year_input.setMinimumHeight(35)
        year_input.setText(str(datetime.datetime.now().year))
        vbox.addWidget(year_input)

        b = QPushButton('Создать журнал')
        b.setObjectName('button-white')
        b.clicked.connect(self._create_journal(main_window, year_input))
        vbox.addWidget(b)

        b = QPushButton('Назад')
        b.setObjectName('button')
        b.clicked.connect(functools.partial(parent.set_current_index, 0))
        vbox.addWidget(b)

        vbox.addStretch()
        layout.addLayout(vbox)
        layout.addStretch()
        self.setLayout(layout)

    @staticmethod
    def _open(path):
        name = os.name

        if name == 'posix':
            subprocess.call(['xdg-open', path])
        elif name == 'nt':
            os.startfile(path)
        else:
            raise AttributeError('Unknown system')

    @staticmethod
    def _get_reports(year):
        return db.SESSION.query(db.Report).filter(
            extract('year', db.Client.examined) == year,
        ).all()

    @staticmethod
    def _get_conclusion_from_report(report):
        conclusion = []
        doc = load(report.path)
        paragraphs = doc.getElementsByType(text.P)
        for i in range(len(paragraphs)):
            if teletype.extractText(paragraphs[i]).strip().startswith('Заключение:'):
                conclusion.append(
                    teletype.extractText(paragraphs[i]).replace('Заключение:', '').strip()
                )

        return '; '.join(conclusion)

    def _get_data_from_report(self, report):
        data = [
            report.client.examined,
            '{} {} {}'.format(
                report.client.surname,
                report.client.name,
                report.client.patronymic,
            ),
            report.client.date_of_birth,
            report.client.address,
            self._get_conclusion_from_report(report),
        ]

        return data

    def _create_journal(self, main_window, year_input):
        def _f():
            try:
                year = int(year_input.text())
                if year > datetime.datetime.now().year or year < 1900:
                    raise ValueError
            except ValueError:
                main_window.create_alert('Неправильно введен год')
                return

            reports = self._get_reports(year)
            journal = []
            for report in reports:
                journal.append(self._get_data_from_report(report))

            path = os.path.join(options.REPORTS_DIR, 'Журнал {}.csv'.format(year))
            with open(path, 'w', encoding='utf8') as journal_file:
                journal_file_writer = csv.writer(journal_file, quotechar='"')
                journal_file_writer.writerow(['Дата', 'ФИО', 'Дата Рождения', 'Адрес', 'Заключение'])
                for row in journal:
                    journal_file_writer.writerow(row)

            self._open(path)

        return _f
