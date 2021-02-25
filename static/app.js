const boggle = new Boggle();

let $form = $('#boggle-guess-input');
$form.on('submit', (e) => {
    e.preventDefault();
    let $input = $('#guess');
    let guess = $input.val();
    $input.val('')

    if (boggle.gameOver) {
        boggle.resetGame()
        return;
    } else {
        if (guess != '') {
            boggle.submitGuess(guess);
        }
    }

});


let $resetBtn = $('#reset');
$resetBtn.on('click', () => {
    boggle.resetGame();
});