let score = 0;
let gameOver = false;

let $form = $('#boggle-guess-input');
$form.on('submit', (e) => {
    e.preventDefault();
    let $input = $('#guess');
    let guess = $input.val();
    $input.val('')
    submitGuess(guess);

})

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

    if (result == RESULT_OK) {
        //result was good
        addToScore(word.length);
    } else if (result == RESULT_NOT_ON_BOARD) {
        //result was not on board
        alert('Sorry, I don\'t See ' + guess + ' on my board, try again ');
    } else if (result = RESULT_NOT_A_WORD) {
        //result not a word
        alert('I dont think thats a word...');
    }
}

function addToScore(points) {
    score += points;
    updateScoreBoard();
}
function updateScoreBoard() {
    $scoreBoard = $('#score-board');
    $scoreBoard.text(score);
}