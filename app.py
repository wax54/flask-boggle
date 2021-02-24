from flask import Flask, session, request, render_template as render, jsonify
from boggle import Boggle


app = Flask(__name__)

app.config["SECRET_KEY"] = "a secret key"

boggle_game = Boggle()


@app.route("/")
def display_boggle_game():
    """gets the boggle game and displays it for the user"""
    board = get_board()
    return render("boggle-board.html", board=board)


@app.route("/guess", methods=["POST"])
def guess_word():
    """  """
    guess = request.json.get("guess")
    result = boggle_game.check_valid_word(get_board(), guess)
    return jsonify({"result": result})


@app.route("/game-over", methods=["POST"])
def game_over():
    session.pop("board", None)
    increment_play_count()

    score = int(request.json.get("score"))
    high_score = update_high_score(score)
    return jsonify({"high_score": high_score, "num_of_plays": session["play_count"]})


def update_high_score(score):
    if score > session.get("high_score", 0):
        session["high_score"] = score
    return session.get("high_score", 0)


def increment_play_count():
    if session.get("play_count"):
        print(session["play_count"])
    session["play_count"] = 1


def reset_board():
    board = boggle_game.make_board()
    session["board"] = board


def get_board():
    """returns the current boggle game board. If none in session already, it makes a new one, stores it in the session, then returns it"""
    if session.get("board"):
        return session["board"]
    else:
        board = boggle_game.make_board()
        session["board"] = board
        return board
