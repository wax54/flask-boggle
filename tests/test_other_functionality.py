from unittest import TestCase
from app import app, increment_play_count, update_high_score, make_board, get_board
from flask import session
from boggle import Boggle


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
    def test_high_score_at_game_over(self):
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


    def test_update_high_score(self):
        with app.test_client() as client:
            client.get('/')
            self.assertEqual(session.get('high_score'), None)
            update_high_score(-3)
            self.assertEqual(session.get('high_score'), 0)
            
            update_high_score(0)
            self.assertEqual(session.get('high_score'), 0)
            
            update_high_score(5)
            self.assertEqual(session.get('high_score'), 5)
            
            update_high_score(4)
            self.assertEqual(session.get('high_score'), 5)
            
            update_high_score(7)
            self.assertEqual(session.get('high_score'), 7)

class BoggleBoardTests(TestCase):
        
    def test_make_board(self):
        with app.test_client() as client:
            #setup
            client.get('/')
            first_board = session.get('board')
            session['used_words'] = ['a','o','hello']
            
            #the main Event
            new_board = make_board()
            
            #the Tests
            self.assertNotEqual(first_board, new_board)
            self.assertEqual(session.get('board'), new_board)
            self.assertEqual(session.get('used_words'),[])
            
    def test_get_board_gets_curr_board(self):
        with app.test_client() as client:
            #setup
            client.get('/')
            first_board = session.get('board')
            session['used_words'] = ['a','o','hello']
            
            #the main Event
            board = get_board()
            
            #the Tests
            self.assertEqual(first_board, board)
            self.assertEqual(session.get('board'), board)
            self.assertEqual(session.get('used_words'),['a','o','hello'])

    def test_get_board_when_no_board_in_session(self):
        with app.test_client() as client:
            #setup
            client.get('/')
            session.pop('board')
            self.assertEqual(session.get('board'), None)
            
            #the main Event
            board = get_board()
            
            #the get_board made a board, stored it in session and returned it to us
            self.assertEqual(session.get('board'), board)
            
            