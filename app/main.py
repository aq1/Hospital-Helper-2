# -*- coding: UTF-8 -*-

import options
from model import db, logic, report, exceptions


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

    for i in items:
        i.template = 'norma'
        i['asd'] = 2

    r = report.Report(items)
    r.get_templates()
    # for i, o in enumerate(objects):
    #     print(i, o.get_for_template())


if __name__ == '__main__':
    init()
