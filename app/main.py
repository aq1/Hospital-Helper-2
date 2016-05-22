import options

from gui import main as gui
from model import (db, logic, exceptions, localization)


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

    # for i in items:
    #     for j in range(25):
    #         t, _ = db.Template.get_or_create(item_id=i.id, name='%s %s' % (i.name, j), body='Тело', conclusion='Заключение')
    # db.SESSION.flush()

    gui.init(items)


if __name__ == '__main__':
    init()


    # c = db.SESSION.query(db.Client).filter(db.Client.id < 200).count() - 100
    # x = db.SESSION.query(db.Client).filter(db.Client.id < 200).order_by(db.Client.id)
    # print(c, x[0].id, x[-1].id)
    # for _ in range(500):
        # c = db.Client(name='Иван', surname='Иванов', patronymic='Иванович', user_id=1, age=30)
        # c.save()
    # id = Column(Integer, primary_key=True)
    # surname = Column(String, nullable=False, default='')
    # name = Column(String, nullable=False, default='')
    # patronymic = Column(String, nullable=False, default='')
    # date_of_birth = Column(Date)
    # hr = Column(SmallInteger, nullable=False, default=0)
    # height = Column(SmallInteger, nullable=False, default=0)
    # weight = Column(SmallInteger, nullable=False, default=0)
    # examined = Column(Date, nullable=False, default=datetime.datetime.now)
    # sent_by = Column(String, nullable=False, default='')

    # user_id = Column(ForeignKey('user.id'), nullable=False)
    # user = relationship('User', backref='klient')
