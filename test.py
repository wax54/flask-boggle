from unittest import TestCase
from app import app, increment_play_count
from flask import session
from boggle import Boggle


# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class BoggleHomePageTests(TestCase):
    def test_initial_load(self):
        with app.test_client() as client:
            res = client.get('/')
            self.assertEqual(res.status_code, 200)
            html = res.get_data(as_text=True)
            
            self.assertIn('<h1 class="title">BOGGLE!</h1>', html)
            #the board in the session should have 5 arrays inside
            self.assertEqual(len(session['board']), 5)
            
    def test_page_refresh_yields_new_board(self):
        with app.test_client() as client:
            res = client.get('/')
            first_load = res.get_data(as_text=True)

            res = client.get('/')
            second_load = res.get_data(as_text=True)
            
            #seperate loads should yield seperate boards, and therefor, seperate files
            self.assertNotEqual(first_load, second_load)

class GuessPageTests(TestCase):
        
    def test_valid_guess(self):
        with app.test_client() as client:
            res = client.get('/')
            board = session['board']
            valid_guess = self.get_valid_guess(board).upper()
            res = client.post("/guess", json={'guess' : valid_guess})
            self.assertEqual(res.json['result'], 'ok')
    def test_valid_guess_case_insensitive(self):
        with app.test_client() as client:
            res = client.get('/')
            board = session['board']
            valid_guess = self.get_valid_guess(board).lower()
            res = client.post("/guess", json={'guess' : valid_guess})
            self.assertEqual(res.json['result'], 'ok')
    
    def test_not_on_board_guess(self):
        with app.test_client() as client:
            res = client.get('/')
            not_on_board_guess = "Helminthocladiaceae"
            res = client.post("/guess", json={'guess' : not_on_board_guess})
            self.assertEqual(res.json['result'], 'not-on-board')
            
    def test_not_a_word_guess(self):
        with app.test_client() as client:
            res = client.get('/')
            not_a_word_guess = "gradadanshg"
            res = client.post("/guess", json={'guess' : not_a_word_guess})
            self.assertEqual(res.json['result'], 'not-a-word')
            
    def test_repeated_guess(self):
        with app.test_client() as client:
            res = client.get('/')
            board = session['board']
            valid_guess = self.get_valid_guess(board).lower()
            
            res = client.post("/guess", json={'guess' : valid_guess})
            self.assertEqual(res.json['result'], 'ok')
            
            res = client.post("/guess", json={'guess' : valid_guess})
            self.assertEqual(res.json['result'], 'used-word')
            
    def get_valid_guess(self, board):
        """returns a valid guess from the current board"""
        board_set = set()
        for row in board:
            board_set = board_set | set(row)
        vowels_on_board = set('AEIOU') & board_set
        return vowels_on_board.pop()

class GameOverPageTests(TestCase):
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

class ReshuffleTests(TestCase):
    def test_reshuffle_works_without_root_load(self):
        with app.test_client() as client:
            res = client.get('/reshuffle')
            self.assertEqual(res.status_code, 200)
            html = res.get_data(as_text=True)
            test_string = '<table class="boggle-board">'
            #should load the filled in boggle table
            self.assertIn(test_string, html.strip())
            #should not load the whole boggle page
            self.assertNotIn('<h1 class="title">BOGGLE!</h1>')
            
    def test_reshuffle_sends_unique_tables(self):
        
            with app.test_client() as client:
            res = client.get('/reshuffle')
            first_table = res.get_data(as_text=True)
            
            res = client.get('/reshuffle')
            self.assertEqual(res.status_code, 200)
            second_table = res.get_data(as_text=True)
            self.assertNotEqual(first_table,second_table)
            

class PlayCountTests(TestCase):
    def test_play_count_on_page_load(self):
        with app.test_client() as client:
            res = client.get('/')
            html = res.get_data(as_text=True)
            
            #if no 'play_count' in session, should be zero
            self.assertIn('<span id="play-count">0</span>', html)
            
            
            with client.session_transaction() as change_session:
                change_session['play_count'] = 99
            res = client.get('/')
            html = res.get_data(as_text=True)
            
            #if 'play_count' in session, should be play_count
            self.assertIn('<span id="play-count">99</span>', html)
        
    def test_increment_play_count(self):
        with app.test_client() as client:
            client.get('/')
            self.assertEqual(session.get('play_count'), None)
            increment_play_count()
            self.assertEqual(session.get('play_count'), 1)
            increment_play_count()
            increment_play_count()
            self.assertEqual(session.get('play_count'), 3)

class HighScoreTests(TestCase):
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

