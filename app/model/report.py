import os
import datetime
from collections import OrderedDict

from odf.opendocument import OpenDocumentText
from odf.style import Style, TextProperties
from odf.text import H, P, Span

import options
from model import db, exceptions


class Report:

    def __init__(self, user, items):

        self.user = user

        if not self.user.organization:
            self.user.organization = db.SESSION.query(db.Organization).get(self.user.organization_id)

        self.template_groups = OrderedDict()

        for item in items:
            if item.name == options.CLIENT_TABLE_NAME:
                self.client = self._get_client(item)
            if not self.template_groups.get(item.group):
                self.template_groups[item.group] = []

            self.template_groups[item.group].append(item)

    def _get_client(self, item):
        # It's hardcoded for now
        # FIXME: change it in future'
        return db.Client(surname=item['familiia'],
                         name=item['imia'],
                         patronymic=item['otchestvo'],
                         age=item['vozrast'],
                         hr=item['chss'],
                         height=item['rost'],
                         weight=item['ves'],
                         examined=datetime.date.today(),
                         user_id=self.user.id)

    def _get_header(self):

        return self.user.organization.header or ''

    def _get_footer(self):

        if not self.user:
            return ''
        else:
            return '{} {} {} {}'.format(datetime.datetime.now().strftime('%d.%m.%Y'),
                                        self.user.surname,
                                        self.user.name,
                                        self.user.patronymic)

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

    def render_and_save(self):
        path = os.path.join(options.REPORTS_DIR, os.sep.join(datetime.date.today().isoformat().split('-')))
        if not os.path.exists(path):
            os.makedirs(path)

        self.client.save()

        document = self.render()
        document.save(os.path.join(path, '{}.odt'.format(self.user)))
        report = db.Report(path=path, client_id=self.client.id)
        report.save()
        return report
