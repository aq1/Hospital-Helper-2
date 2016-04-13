import datetime
from collections import OrderedDict

from odf.opendocument import OpenDocumentText
from odf.style import Style, TextProperties
from odf.text import H, P, Span

from model import db, exceptions


class Report:

    def __init__(self, items, user):

        self.user = user

        if self.user:
            self.organization = db.SESSION.query(db.Organization).get(self.user.organization_id)
        else:
            self.organization = None

        self.template_groups = OrderedDict()

        for item in items:
            if not self.template_groups.get(item.group):
                self.template_groups[item.group] = []

            self.template_groups[item.group].append(item)

    def _get_header(self):

        if not self.organization:
            return ''
        else:
            return self.organization.header

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
