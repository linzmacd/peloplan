from unittest import TestCase
from server import app
from model import connect_to_db, db, test_data
import os
# from flask import session

class FlaskTests(TestCase):

    def setUp(self):
        '''Stuff to do before every test.'''        
        self.client = app.test_client()
        app.config['TESTING'] = True

        os.system('dropdb testdb')
        os.system('createdb testdb')
        connect_to_db(app, 'postgresql:///testdb')

        # Create tables and add sample data
        db.create_all()
        test_data()

    def tearDown(self):
        '''Stuff to do after each test.'''
        db.session.remove()
        db.drop_all()
        db.engine.dispose()

    def test_homepage(self):
        '''Tests homepage.'''
        result = self.client.get('/')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<h1>Welcome to PeloPlan!</h1>', result.data)

    def test_login(self):
        '''Tests login page.'''
        result = self.client.post('/login',
                                data={'email': 'janedoe@gmail.com', 
                                      'password': 'password123'},
                                follow_redirects=True)
        self.assertIn(b'<h2>Peloton Log In</h2>', result.data)


if __name__ == '__main__':
    import unittest
    unittest.main()