import os
import datetime
import functools
import subprocess

from odf import (
    opendocument,
    style,
    text,
    teletype,
    table,
)

from odf.opendocument import load
from sqlalchemy import extract

from PyQt5.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QLineEdit,
    QComboBox,
)

from app.model import db
from app import options


class JournalWidget(QFrame):
    months = (
        'Январь',
        'Февраль',
        'Март',
        'Апрель',
        'Май',
        'Июнь',
        'Июль',
        'Август',
        'Сентябрь',
        'Октябрь',
        'Ноябрь',
        'Декабрь',
    )

    def __init__(self, main_window, parent):
        super().__init__()
        self.main_window = main_window
        now = datetime.datetime.now()
        self.year = now.year
        self.month = now.month - 1
        self.doctors = [
            (d.id, '{} {}.{}. - {}'.format(d.surname, d.name[0], d.patronymic[0], d.organization.name))
            for d in db.SESSION.query(db.User).all()
            if not (d.deleted or d.organization.deleted)
        ]

        self._create_layout(main_window, parent)

    def _create_layout(self, main_window, parent):
        layout = QHBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(20)

        vbox = QVBoxLayout()
        vbox.setContentsMargins(15, 15, 15, 15)
        vbox.setSpacing(20)

        hbox = QHBoxLayout()
        year_input = QLineEdit()
        year_input.setMinimumHeight(35)
        year_input.setText(str(self.year))
        year_input.textChanged.connect(self._set_year)
        hbox.addWidget(year_input)

        month_input = QComboBox(self, maxVisibleItems=6)
        month_input.view().setSpacing(6)
        list(map(month_input.addItem, self.months))
        month_input.setCurrentIndex(self.month)
        month_input.activated[str].connect(self._set_month)
        hbox.addWidget(month_input)

        vbox.addLayout(hbox)

        self.doctor_input = QComboBox(self, maxVisibleItems=4)
        self.doctor_input.view().setSpacing(6)
        list(map(self.doctor_input.addItem, [d[1] for d in self.doctors]))
        vbox.addWidget(self.doctor_input)

        hbox = QHBoxLayout()
        b = QPushButton('Назад')
        b.setObjectName('button')
        b.clicked.connect(functools.partial(parent.set_current_index, 0))
        hbox.addWidget(b)

        b = QPushButton('Создать журнал')
        b.setObjectName('button-white')
        b.clicked.connect(self._create_journal(main_window))
        hbox.addWidget(b)

        vbox.addStretch()
        vbox.addLayout(hbox)

        vbox.addStretch()
        layout.addLayout(vbox)
        layout.addStretch()
        self.setLayout(layout)

    def _set_year(self, text):
        self.year = text

    def _set_month(self, text):
        self.month = self.months.index(text)

    @property
    def doctor(self):
        return self.doctors[self.doctor_input.currentIndex()]

    @staticmethod
    def _open(path):
        name = os.name

        if name == 'posix':
            subprocess.call(['xdg-open', path])
        elif name == 'nt':
            os.startfile(path)
        else:
            raise AttributeError('Unknown system')

    def _get_reports(self):
        q = db.SESSION.query(db.Report).join(db.Client).join(db.User)
        q = q.filter(
            extract('year', db.Client.examined) == self.year,
            extract('month', db.Client.examined) == self.month + 1,
        )
        q = q.filter(db.Client.user_id == self.doctor[0])
        return q

    @staticmethod
    def _get_conclusion_from_report(report):
        conclusion = []
        try:
            doc = load(report.path)
        except FileNotFoundError:
            return 'Не найдено'
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

    def _write_journal(self, journal):
        path = os.path.join(
            options.REPORTS_DIR, 'Журнал {} {} {}.odt'.format(
                self.year,
                self.months[self.month],
                self.doctor[1],
            )
        )

        doc = opendocument.OpenDocumentText()
        table_style = style.Style(name='tableStyle', family='table', masterpagename='masterQ')
        page_layout = style.PageLayout(name='pageStyle')
        page_layout.addElement(style.PageLayoutProperties(
            printorientation='landscape',
            margin='0cm',
            pagewidth='290cm',
            pageheight='21cm',
        ))
        master_q = style.MasterPage(name='masterQ', pagelayoutname=page_layout)
        doc.automaticstyles.addElement(table_style)
        doc.automaticstyles.addElement(page_layout)
        doc.masterstyles.addElement(master_q)

        journal = (
                [['Дата', 'ФИО', 'Дата Рождения', 'Адрес', 'Заключение']] +
                journal
        )

        _table = table.Table(name='journal')
        _table.addElement(table.TableColumn(numbercolumnsrepeated=len(journal[0])))
        for data in journal:
            row = table.TableRow()
            _table.addElement(row)
            for col in data:
                cell = table.TableCell(valuetype='string')
                cell.addElement(text.P(text=str(col or '')))
                row.addElement(cell)

        doc.text.addElement(_table)
        try:
            doc.save(path)
        except PermissionError:
            self.main_window.create_alert(
                'Файл журнала используется.\nЗакройте его и создайте снова.'
            )
            return
        self._open(path)

    def _create_journal(self, main_window):
        def _f():
            try:
                year = int(self.year)
                if year > datetime.datetime.now().year or year < 1900:
                    raise ValueError
            except ValueError:
                main_window.create_alert('Неправильно введен год')
                return

            reports = self._get_reports()
            journal = []
            for report in reports:
                journal.append(self._get_data_from_report(report))

            self._write_journal(journal)

        return _f
