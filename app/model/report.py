# -*- coding: UTF-8 -*-

from collections import OrderedDict

from odf.opendocument import OpenDocumentText
from odf.style import Style, TextProperties
from odf.text import H, P, Span

from model import db, exceptions


class Report:

    def __init__(self, items):

        self.template_groups = OrderedDict()

        for item in items:
            if item.template and any(item.values()):
                self._add_item(item)

    def _add_item(self, item):
        db_item = db.SESSION.query(db.Item).filter(
            db.Item.name == item.name).first()
        template = db.SESSION.query(db.Template).filter(
            db.Template.item == db_item.id, db.Template.name == item.template).first()

        if not self.template_groups.get(item.group):
            self.template_groups[item.group] = []

        item.template = template
        self.template_groups[item.group].append(item)

    def render(self, strict_mode=False):
        document = OpenDocumentText()

        for _, group in self.template_groups.items():
            conclusion = []

            for item in group:
                document.text.addElement(H(outlinelevel=4, text=item.name))
                if not item.template:
                    if strict_mode:
                        raise exceptions.NoTemplateForItem()
                else:
                    conclusion.append(item.template.conclusion)
                    document.text.addElement(P(text=item.template.body.format(**item.for_template())))

            conclusion = '\n'.join(conclusion)
            document.text.addElement(P(text=conclusion))
            return document


# # Styles
# h1style = Style(name="Heading 1", family="paragraph")
# h1style.addElement(TextProperties(attributes={'fontsize':"24pt",'fontweight':"bold" }))
# s.addElement(h1style)
# # An automatic style
# boldstyle = Style(name="Bold", family="text")
# boldprop = TextProperties(fontweight="bold")
# boldstyle.addElement(boldprop)
# textdoc.automaticstyles.addElement(boldstyle)
# # Text
# textdoc.text.addElement(h)
# boldpart = Span(stylename=boldstyle, text="This part is bold. ")
# p.addElement(boldpart)
# p.addText("This is after bold.")
# textdoc.text.addElement(p)
# textdoc.save("myfirstdocument.odt")
