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
            
            
    def test_game_over(self):
        with app.test_client() as client:
            client.get('/')
            self.assertIs(session.get("play_count"), None)
            self.assertIs(session.get('high_score'), None)
            # the game over post sent
            res = client.post('/game-over', json={'score':4})
            self.assertEqual(session.get("play_count"), 1)
            self.assertEqual(session.get("high_score"), 4)
            self.assertIs(session.get('board'), None)
            
            
    def test_high_score(self):
        with app.test_client() as client:
            
            #when no previous high score, and 0 is inputed, 0 is the highest score
            client.get('/')            
            res = client.post('/game-over', json={'score':0})
            self.assertEqual(res.json["high_score"], 0)
            
            client.get('/')
            res = client.post('/game-over', json={'score':4})
            self.assertEqual(res.json["high_score"], 4)
            #if previous high score is higher, the old high score is returned
            client.get('/')
            res = client.post('/game-over', json={'score':3})
            self.assertEqual(res.json["high_score"], 4)
            
            client.get('/')
            res = client.post('/game-over', json={'score':10})
            self.assertEqual(res.json["high_score"], 10)
            
