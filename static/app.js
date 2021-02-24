let score = 0;
let gameOver = false;
const GAME_LENGTH = 6000;
let timeLeft;
let gameTimer;
startTimer();


let $form = $('#boggle-guess-input');
$form.on('submit', (e) => {
    e.preventDefault();
    let $input = $('#guess');
    let guess = $input.val();
    $input.val('')

    if (gameOver) {
        resetGame()
        return;
    } else {
        if (guess != '') {
            submitGuess(guess);
        }
    }

});


let $resetBtn = $('#reset');
$resetBtn.on('click', resetGame);

async function submitGuess(guess) {
    res = await axios({
        url: '/guess',
        method: 'POST',
        data: { guess }
    });
    result = res.data.result;
    handleResults(result, guess);
}

function handleResults(result, word) {
    const RESULT_OK = "ok";
    const RESULT_NOT_ON_BOARD = "not-on-board";
    const RESULT_NOT_A_WORD = "not-a-word";
    const RESULT_USED_WORD = "used-word";

    if (result == RESULT_OK) {
        //result was good
        addToScore(word.length);
    } else if (result = RESULT_USED_WORD) {
        //word has already been used before
        alert('I\'ve already given you points for that word!');
    }
    else if (result == RESULT_NOT_ON_BOARD) {
        //result was not on board
        alert('Sorry, I don\'t See ' + word + ' on my board, try again ');
    }
    else if (result = RESULT_NOT_A_WORD) {
        //result not a word
        alert('I dont think thats a word...');
    }
}

function addToScore(points) {
    score += points;
    updateScoreBoard();
}

async function setGameOver() {
    gameOver = true;
    res = await axios({
        url: '/game-over',
        method: 'POST',
        data: { score }
    });
    let { high_score, num_of_plays } = res.data;

    updateHighScore(high_score);
    updatePlayCount(num_of_plays);

    clearInterval(gameTimer);
}

function startTimer() {
    if (gameTimer) {
        clearInterval(gameTimer);
    }
    timeLeft = GAME_LENGTH;
    downCountTimer()
    gameTimer = setInterval(downCountTimer, 1000);
}



async function resetGame() {
    res = await axios({
        url: '/reshuffle',
        method: 'GET'
    });

    $board = $('#game-board');
    $board.html(res.data);

    gameOver = false;
    score = 0;
    updateScoreBoard();
    startTimer();
}

function downCountTimer() {
    updateHTMLCounter();
    if (timeLeft == 0) {
        setGameOver();
        return;
    }
    timeLeft--;
}

function updateScoreBoard() {
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

function updateHTMLCounter() {
    $timer = $('#timer');
    if (timeLeft > 0) {
        html = 'You Have ' + timeLeft + ' ';
        if (timeLeft === 1) html += ' Second Left';
        else html += 'Seconds Left';
    } else html = 'Your Time Is Up!';

    $timer.html(html);
}