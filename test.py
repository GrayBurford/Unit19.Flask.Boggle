from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle

# to run tests:
# python -m unittest test.py

class FlaskTests(TestCase):

    def setUp (self):
        """Initializes this stuff before every function test"""
        self.client = app.test_client() # sets client to a variable: needed to test actions between pages and routes
        app.config['TESTING'] = True
        app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

    def test_homepage(self):
        """Tests that info is in the session and HTML is displayed"""        
        # can also write: with app.test_client() as client:
        # test by running: python -m unittest test.py
        with self.client:
            response = self.client.get('/')
            html = response.get_data(as_text=True)
            print(response.data) # response is essentially our index.html file
            self.assertIn('Times played: 0', html)
            self.assertIsNone(session.get('highscore'))
            self.assertIn('Time left:', html)
            self.assertIn('High score: 0', html)
            self.assertIsNone(session.get('times_played'))
            self.assertIn('Current score:', html)
            self.assertIn('Current message:', html)
            self.assertIn('Words found', html)
            self.assertIn('board', session)

    def test_valid_word(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["C", "A", "T", "T", "T"], 
                                 ["C", "L", "T", "T", "T"], 
                                 ["C", "A", "L", "T", "T"], 
                                 ["C", "A", "T", "A", "T"], 
                                 ["C", "A", "T", "T", "T"]]
        response = self.client.get('/check-word?word=tall')
        self.assertEqual(response.json['result'], 'ok')

    def test_word_not_on_board(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["C", "A", "T", "T", "T"], 
                                 ["C", "L", "T", "T", "T"], 
                                 ["C", "A", "L", "T", "T"], 
                                 ["C", "A", "T", "A", "T"], 
                                 ["C", "A", "T", "T", "T"]]
        response = self.client.get('/check-word?word=flute')
        self.assertEqual(response.json['result'], 'not-on-board')

    def test_word_not_english(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["C", "A", "T", "T", "T"], 
                                 ["C", "L", "T", "T", "T"], 
                                 ["C", "A", "L", "T", "T"], 
                                 ["C", "A", "T", "A", "T"], 
                                 ["C", "A", "T", "T", "T"]]
        response = self.client.get('/check-word?word=sdkfghu')
        self.assertEqual(response.json['result'], 'not-word')