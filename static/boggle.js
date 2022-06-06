class BoggleGame {
    constructor (boardId, secs = 60) {
        this.secs = secs;
        this.board = $("#" + boardId);
        this.words = new Set(); // list of unique items to append found words
        this.score = 0;
        this.showTimer()
        this.countDown = setInterval(this.tick.bind(this), 1000)
        $('.form').on('submit', this.handleSubmit.bind(this));
        // $('.form', this.board).on('submit', this.handleSubmit.bind(this));
    }

    async handleSubmit(e) {
        e.preventDefault();
        const $word = $(".form-word-input")
        let word = $word.val() // val of user input
        console.log("User input is: " + word)
        if (!word) return // if no form input, return/do nothing
        if (this.words.has(word)) {
            this.showMessage(`You already found ${word}, 'err'`)
            return
        }
        // send word to the "server" and check for type of response
        const response = await axios.get('/check-word', { params : {word:word}});
        console.log(response)

        if (response.data.result === 'not-word') {
            this.showMessage(`${word} is not a valid English word`, 'err')
        }
        else if (response.data.result === 'not-on-board') {
            this.showMessage(`${word} is not a valid word on this board`, 'err')
        }
        else {
            this.showWord(word);
            this.score += word.length;
            this.showScore();
            this.words.add(word);
            this.showMessage(`Added: ${word}`, 'ok')
        }

        // empty input and focus on input after every submit
        $word.val("").focus(); 
    }

    // Dicplay a message passed in from handleSubmit() to the DOM
    showMessage(msg, cls) {
        $(".msg")
        // $(".msg", this.board)
      .text(msg)
      .removeClass()
      .addClass(`msg ${cls}`);
    }

    // if word is valid from handleSubmit(), append it to the DOM list
    showWord(word) {
        $('.words-list').append($('<li>', { text:word}))
        // $('.words-list', this.board).append($('<li>', { text:word}))
    }

    // Displays/updates score in the DOM
    showScore() {
        $('.score').text(this.score);
        // $('.score', this.board).text(this.score);
    }

    // displays/updates timer in the DOM
    showTimer() {
        $('.time').text(this.secs)
    }

    // decrease secs by 1 every 1000ms, and re-update showTimer()
    // if timer hits 0, hide the form (don't allow more guesses), prepend message to DOM, and run gameOver()
    tick() {
        this.secs -= 1;
        this.showTimer();
        if (this.secs === 0) {
            clearInterval(this.countDown);
            $('.form').hide();
            $('.data-div').prepend("<p>TIME IS UP! GAME OVER!</p>")
            this.gameOver();
        }
    }

    // posts game's score to the server and checks if highscore needs to be updated.
    async gameOver() {
        console.log("Game over from inside gameOver")
        await axios.post('/game-over', 
        {
            currScore : this.score,
            testingJson : "Test",
            remainingSecs : this.secs
        })

    }

}

let game = new BoggleGame("boggle");

