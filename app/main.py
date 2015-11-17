# -*- coding: UTF-8 -*-

import options
from model import db, logic, exceptions


def convert_structure_to_objects(structure):
    parser = logic.Parser()
    object_factory = logic.ObjectFactory

    parsed_structure = parser.parse_structure(structure)

    objects = []
    names = set()
    for i, item in enumerate(parsed_structure, 1):

        names.add(item['name'])
        objects.append(object_factory.get_object(item))
        if i != len(names):
            raise exceptions.NonUniqueObjectNames(item['name'])

    return objects


def init():
    try:
        structure = db.SESSION.query(db.KeyValue).get(options.STRUCTURE_KEY)
        structure = structure.value
    except (AttributeError, db.exc.OperationalError):
        structure = db.KeyValue(key=options.STRUCTURE_KEY,
                                value=options.INIT_STRUCTURE)
        db.SESSION.add(structure)
        structure = structure.value

    objects = convert_structure_to_objects(structure)
    db.create_db()
    # for i, o in enumerate(objects):
    #     print(i, o.get_for_template())


if __name__ == '__main__':
    init()
