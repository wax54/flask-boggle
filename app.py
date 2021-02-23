from flask import Flask, session, render_template as render
from boggle import Boggle


app = Flask(__name__)

app.config["SECRET_KEY"] = "a secret key"

boggle_game = Boggle()

@app.route('/')
def display_boggle_game():
    """gets the boggle game and displays it for the user"""
    board = get_boggle_game()
    return render('boggle-board.html', board=board)

def get_boggle_game():
    """returns the current boggle game board. If none in session already, it makes a new one, stores it in the session, then returns it"""
    if len(session['board']):
        return session['board']
    else:
        board = boggle_game.make_board()
        session['board'] = board
        return board