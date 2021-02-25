from flask import Flask, session, request, render_template as render, jsonify, redirect
from boggle import Boggle


app = Flask(__name__)

app.config["SECRET_KEY"] = "a secret key"

boggle_game = Boggle()


@app.route("/")
def display_boggle_game():
    """gets the whole boggle page and returns it to the user"""
    board = make_board()
    play_count = session.get("play_count", 0)
    high_score = session.get("high_score", 0)
    return render(
        "boggle-page.html", board=board, play_count=play_count, high_score=high_score
    )


@app.route("/guess", methods=["POST"])
def guess_word():
    """operates on a string retrieved from request.json['guess']
    checks if that word is a valid word in the current game and
    returns the result of that check.
    possible results are:
    "ok"
    "not-on-board"
    "not-a-word"
    "used-word"
    """
    guess = request.json.get("guess")
    guess = guess.strip()
    used_words = session["used_words"]
    result = boggle_game.check_valid_word(get_board(), used_words, guess)
    if result == "ok":
        used_words.append(guess.upper())
        session["used_words"] = used_words
    return jsonify({"result": result})


@app.route("/game-over", methods=["POST"])
def game_over():
    """ marks another game well played. 
    Discards the board since it's invalid now
    takes the final score and updates the high score
    returns high_score and num_of_plays to the client via json
    """
    session.pop("board", None)
    increment_play_count()
    score = int(request.json.get("score"))
    high_score = update_high_score(score)
    return jsonify({"high_score": high_score, "num_of_plays": session["play_count"]})


@app.route("/reshuffle")
def reset_board():
    """ creates and returns a new boggle board table to the client 
    note: this is just the table, not the whole boggle page
    """
    board = make_board()
    return render("boggle-board.html", board=board)


def update_high_score(score):
    """ updates the session['high_score'] based on latest score data
    returns new highest score
    """
    high_score = session.get("high_score", 0)
    if score > high_score:
        high_score = score
    session["high_score"] = high_score
    return high_score


def increment_play_count():
    """ increments session['play_count'] """
    plays = session.get("play_count", 0)
    session["play_count"] = plays + 1


def make_board():
    """gets a new boggle board from the Boggle class
    sets session['board'] to the new board
    sets session['used_words'] to an empty array
    returns the new board
    """
    board = boggle_game.make_board()
    session["board"] = board
    # resets the used words since we have a new board
    session["used_words"] = []
    return board


def get_board():
    """returns the current boggle game board. 
    If none in session already, it makes a new one, 
    stores it in the session, then returns it"""
    if session.get("board"):
        return session["board"]
    else:
        return make_board()
