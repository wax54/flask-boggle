

class Boggle {
    constructor(gameLength = 60) {
        this.score = 0;
        this.gameOver = false;
        this.GAME_LENGTH = gameLength;
        this.timeLeft;
        this.gameTimer;
        this.startTimer();
    }

    startTimer() {
        if (this.gameTimer) {
            clearInterval(this.gameTimer);
        }
        this.timeLeft = this.GAME_LENGTH;
        this.downCountTimer()
        this.gameTimer = setInterval(this.downCountTimer.bind(this), 1000);
    }

    downCountTimer() {
        updateHTMLCounter(this.timeLeft);

        if (this.timeLeft == 0) {
            this.setGameOver();
            return;
        }
        this.timeLeft -= 1;
    }


    async setGameOver() {
        this.gameOver = true;
        clearInterval(this.gameTimer);
        const score = this.score;
        const res = await axios({
            url: '/game-over',
            method: 'POST',
            data: { score }
        });

        let { high_score, num_of_plays } = res.data;
        updateHighScore(high_score);
        updatePlayCount(num_of_plays);
    }

    async submitGuess(guess) {
        const res = await axios({
            url: '/guess',
            method: 'POST',
            data: { guess }
        });
        result = res.data.result;
        this.handleResults(result, guess);
    }


    handleResults(result, word) {
        const RESULT_OK = "ok";
        const RESULT_NOT_ON_BOARD = "not-on-board";
        const RESULT_NOT_A_WORD = "not-a-word";
        const RESULT_USED_WORD = "used-word";

        if (result == RESULT_OK) {
            //result was good
            this.addToScore(word.length);
        } else if (result == RESULT_USED_WORD) {
            //word has already been used before
            alertUser('I\'ve already given you points for that word!');
        }
        else if (result == RESULT_NOT_ON_BOARD) {
            //result was not on board
            alertUser('Sorry, I don\'t See ' + word + ' on my board, try again ');
        }
        else if (result == RESULT_NOT_A_WORD) {
            //result not a word
            alertUser('I dont think thats a word...');
        }
    }


    addToScore(points) {
        this.score += points;
        updateScoreBoard(this.score);
    }

    async resetGame() {
        const res = await axios({
            url: '/reshuffle',
            method: 'GET'
        });

        const $board = $('#game-board');
        $board.html(res.data);

        this.gameOver = false;
        this.score = 0;
        updateScoreBoard(this.score);
        this.startTimer();
    }

}

function updateHTMLCounter(timeLeft) {
    const $timer = $('#timer');
    let html = '';
    if (timeLeft > 0) {
        html = 'You Have ' + timeLeft + ' ';
        if (timeLeft === 1) html += ' Second Left';
        else html += 'Seconds Left';
        if (timeLeft < 10) html += '!';
    } else html = 'Your Time Is Up!';
    $timer.html(html);
}

function updateScoreBoard(score) {
    $scoreBoard = $('#score-board');
    text = score;
    // text = 'You Have ' + score + ' ';
    // if (score === 1) text += 'Point';
    // else text += 'Points';

    $scoreBoard.text(text);
}

function updatePlayCount(playCount) {
    console.log(playCount);
    $playCount = $('#play-count');
    // text = 'You Have played ' + playCount + ' ';
    // if (playCount === 1) text += 'time';
    // else text += 'times';
    text = playCount;
    $playCount.text(text);
}

function updateHighScore(highScore) {
    $highScoreBoard = $('#high-score');
    // text = 'Your High Score is ' + highScore + ' ';
    // if (highScore === 1) text += 'Point';
    // else text += 'Points';
    text = highScore;
    $highScoreBoard.text(text);
}

function alertUser(text) {
    $infoBar = $('#user-info');
    $infoBar.text(text);
    $infoBar.show();
    setTimeout(() => { $infoBar.hide() }, 1500)
}