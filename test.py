from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!

    def test_initial_load(self):
        with app.test_client() as client:
            res = client.get('/')
            self.assertEqual(res.status_code, 200)
            html = res.get_data(as_text=True)
            
            self.assertIn('<h1 class="title">BOGGLE!</h1>', html)
            #the board in the session should have 5 arrays inside
            self.assertEqual(len(session['board']), 5)
            
