import unittest

from sqlalchemy.orm import exc

from app.model import db, exceptions


class TestModel(unittest.TestCase):
    user_args = {
        'surname': 'Test',
        'name': 'Test Name',
        'patronymic': 'Test'
    }

    def _clean_db(self):
        for t in db.Base.metadata.tables:
            db.SESSION.execute('delete from "{}";'.format(t))

    def setUp(self):
        self.organization = db.Organization(name='test', header='')
        self.organization.save()

        self.user = db.User(organization=self.organization, **self.user_args)
        self.user.save()

    def test_get(self):
        with self.assertRaises(exc.NoResultFound):
            db.Template.get(id=1)

        user = db.User.get(id=self.user.id)
        self.assertEqual(user, self.user)

        with self.assertRaises(exc.NoResultFound):
            db.User.get(name='garbage')

        db.User(organization=self.organization, **self.user_args).save()
        with self.assertRaises(exc.MultipleResultsFound):
            db.User.get(name=self.user_args['name'])

    def test_get_or_create(self):
        self._clean_db()
        for _ in range(3):
            db.User(organization=self.organization, **self.user_args).save()

        with self.assertRaises(exc.MultipleResultsFound):
            db.User.get_or_create(name=self.user_args['name'])

        user, created = db.User.get_or_create(id=1)
        self.assertEqual(created, False)

        user, created = db.User.get_or_create(organization=self.organization, name='1', surname='2', patronymic='3')
        self.assertEqual(created, True)
