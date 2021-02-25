from unittest import TestCase
from app import app
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

class ReshufflePageTests(TestCase):
    def test_reshuffle_works_without_root_load(self):
        with app.test_client() as client:
            res = client.get('/reshuffle')
            self.assertEqual(res.status_code, 200)
            html = res.get_data(as_text=True)
            test_string = '<table class="boggle-board">'
            b = session['board']
            test_array = [f"<td>{b[0][0]}</td>", f"<td>{b[0][1]}</td>",f"<td>{b[0][3]}</td>"]
            #should load the filled in boggle table
            self.assertIn(test_string, html)
            for test in test_array:
                self.assertIn(test, html)
            #should not load the whole boggle page
            self.assertNotIn('<h1 class="title">BOGGLE!</h1>',html)
            
    def test_reshuffle_sends_unique_tables(self):
        with app.test_client() as client:
            res = client.get('/reshuffle')
            first_table = res.get_data(as_text=True)
            
            res = client.get('/reshuffle')
            self.assertEqual(res.status_code, 200)
            second_table = res.get_data(as_text=True)
            self.assertNotEqual(first_table,second_table)
