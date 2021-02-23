from flask import Flask, session, render_template
from boggle import Boggle


app = Flask(__name__)

app.config["SECRET_KEY"] = "a secret key"

boggle_game = Boggle()

@app.route('/')
def main_boggle_page():
    board = boggle_game.make_board()
    session['board'] = board
    return render_template('boggle-board.html', board)