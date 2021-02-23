from flask import Flask, session, render_template as render
from boggle import Boggle


app = Flask(__name__)

app.config["SECRET_KEY"] = "a secret key"

boggle_game = Boggle()

@app.route('/')
def main_boggle_page():
    board = boggle_game.make_board()
    session['board'] = board
    print(board)
    return render('boggle-board.html', board=board)