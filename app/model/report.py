import os
import subprocess
import datetime
from collections import OrderedDict, defaultdict

from odf.opendocument import OpenDocumentText
from odf.style import Style, TextProperties, ParagraphProperties
from odf.text import H, P

from app import options
from app.model import db


class Report:

    def __init__(self, user, items):

        self.user = user

        if not self.user.organization:
            self.user.organization = db.SESSION.query(db.Organization).get(self.user.organization_id)

        self.template_groups = OrderedDict()

        for item in items:
            if item.name == options.CLIENT_TABLE_NAME:
                self.client = self._get_client(item)
            if not item.template:
                continue
            if not self.template_groups.get(item.group):
                self.template_groups[item.group] = []

            self.template_groups[item.group].append(item)

    def _get_client(self, item):
        # It's hardcoded for now
        # FIXME: change it in the future'
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

    @staticmethod
    def open(path):
        name = os.name

        if name == 'posix':
            subprocess.call(['xdg-open', path])
        elif name == 'nt':
            os.startfile(path)
        else:
            raise AttributeError('Unknown system')

    def render(self):
        document = OpenDocumentText()

        h1style = Style(name='CenterHeading 1', family='paragraph')
        h1style.addElement(ParagraphProperties(attributes={'textalign': 'center'}))
        h1style.addElement(TextProperties(attributes={'fontsize': '18pt', 'fontweight': 'bold'}))

        header = Style(name='Header', family='paragraph')
        header.addElement(ParagraphProperties(attributes={'textalign': 'center'}))
        header.addElement(TextProperties(attributes={'fontsize': '14pt', 'fontweight': 'bold'}))

        footer = Style(name='Footer', family='paragraph')
        footer.addElement(ParagraphProperties(attributes={'textalign': 'right'}))
        
        h2style = Style(name='CenterHeading 2', family='paragraph')
        h2style.addElement(ParagraphProperties(attributes={'textalign': 'center'}))
        h2style.addElement(TextProperties(attributes={'fontsize': '13pt', 'fontweight': 'bold'}))

        # For bold text
        boldstyle = Style(name='Bold', family='text')
        boldstyle.addElement(TextProperties(attributes={'fontweight': 'bold'}))

        for s in (h1style, h2style, boldstyle, header, footer):
            document.styles.addElement(s)

        document.text.addElement(P(text=self._get_header(), stylename=header))

        keywords = defaultdict(lambda: defaultdict(str))
        for k, group in self.template_groups.items():
            for item in group:
                keywords.update(item.for_template())

        for k, group in self.template_groups.items():
            conclusion = []

            for item in group:
                document.text.addElement(H(outlinelevel=4, text=item.get_verbose_name(), stylename=h2style))
                conclusion.append(item.template.conclusion)
                text = item.template.body.format(**keywords)
                for t in text.splitlines():
                    document.text.addElement(P(text=t))

            conclusion = '\n'.join(conclusion)
            if conclusion:
                conclusion = '{o}{c}'.format(o=options.CONCLUSION, c=conclusion)
                document.text.addElement(P(text=conclusion))

        document.text.addElement(P(text=self._get_footer(), stylename=footer))

        return document

    def render_and_save(self):
        path = os.path.join(options.REPORTS_DIR, *(datetime.date.today().isoformat().split('-')))
        if not os.path.exists(path):
            os.makedirs(path)

        path = os.path.join(path, '{}.odt'.format(self.user))
        document = self.render()
        document.save(path)

        self.client.save()
        report = db.Report(path=path, client_id=self.client.id)
        report.save()
        return report
