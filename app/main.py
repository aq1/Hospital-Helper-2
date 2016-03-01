# -*- coding: UTF-8 -*-

import options

from gui import main as gui
from model import (db, logic, report,
                   exceptions, localization)


def convert_structure_to_items(structure):
    parser = logic.Parser()
    object_factory = logic.ObjectFactory

    parsed_structure = parser.parse_structure(structure)

    items = []
    names = set()
    for i, item in enumerate(parsed_structure, 1):

        names.add(item['name'])
        items.append(object_factory.get_object(item))
        if i != len(names):
            raise exceptions.NonUniqueObjectNames(item['name'])

    return items


def init():
    try:
        structure = db.SESSION.query(db.KeyValue).get(options.STRUCTURE_KEY)
        structure = structure.value
    except (AttributeError, db.exc.OperationalError):
        structure = db.KeyValue(key=options.STRUCTURE_KEY,
                                value=options.INIT_STRUCTURE)
        db.SESSION.add(structure)
        structure = structure.value

    items = convert_structure_to_items(structure)
    db.create_db()

    localization.Localization.install('ru')

    gui.init(items)

    # for i in items:
    #     i.template = 'norma'
    #     i['npv'] = '12'

    # r = report.Report(items, 1)
    # document = r.render()
    # document.save('hello.odt')

if __name__ == '__main__':
    init()
