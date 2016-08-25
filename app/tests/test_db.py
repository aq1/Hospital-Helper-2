import unittest

from sqlalchemy.orm import exc

from app.model import db, exceptions


class TestModel(unittest.TestCase):
    user_args = {
        'surname': 'Test',
        'name': 'Test Name',
        'patronymic': 'Test'
    }

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
