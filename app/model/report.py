import datetime
from collections import OrderedDict

from odf.opendocument import OpenDocumentText
from odf.style import Style, TextProperties
from odf.text import H, P, Span

from model import db, exceptions


class Report:

    def __init__(self, items, doctor_id):

        self.doctor = db.SESSION.query(db.Doctor).get(doctor_id)

        if self.doctor:
            self.hospital = db.SESSION.query(db.Hospital).get(self.doctor.hospital)
        else:
            self.hospital = None

        self.template_groups = OrderedDict()

        for item in items:
            if not self.template_groups.get(item.group):
                self.template_groups[item.group] = []

            self.template_groups[item.group].append(item)

    def _get_header(self):

        if not self.hospital:
            return ''
        else:
            return self.hospital.header

    def _get_footer(self):

        if not self.doctor:
            return ''
        else:
            return '{} {} {} {}'.format(datetime.datetime.now().strftime('%d.%m.%Y'),
                                        self.doctor.surname,
                                        self.doctor.name,
                                        self.doctor.patronymic)

    def render(self, strict_mode=False):
        document = OpenDocumentText()

        document.text.addElement(P(text=self._get_header()))

        for k, group in self.template_groups.items():
            conclusion = []

            for item in group:
                document.text.addElement(H(outlinelevel=4, text=item.get_verbose_name()))
                if not item.template:
                    if strict_mode:
                        raise exceptions.NoTemplateForItem()
                else:
                    conclusion.append(item.template.conclusion)
                    document.text.addElement(P(text=item.template.body.format(**item.for_template())))

            conclusion = '\n'.join(conclusion)
            document.text.addElement(P(text=conclusion))

        document.text.addElement(P(text=self._get_footer()))

        return document
