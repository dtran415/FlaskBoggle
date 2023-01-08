class Boggle {
    constructor() {
        this.time = 60
        this.words = new Set()
        this.score = 0
        this.update_time()
        this.timer = setInterval(this.update_time.bind(this), 1000);
        $('#guess-form').on('submit', this.guess_handler.bind(this))
    }

    async guess_handler(e) {
        e.preventDefault()
        if (this.time == 0) {
            return
        }

        let word = $('#guess').val()
        $('#guess').val('');
        if (this.words.has(word)) {
            $('#check-word-result').attr('class', 'alert alert-warning').text(`${word} already found`)
            return
        }
        let response = await axios.post('/check-word', { word: word })
        $('#guess').val('');
        let result = response.data.result
        switch (result) {
            case 'ok':
                $('#check-word-result').attr('class', 'alert alert-success').text(`${word} added`)
                $('#word-list').append($('<li>').text(word))
                this.words.add(word)
                this.score += word.length
                this.update_score()
                break;
            case 'not-on-board':
                $('#check-word-result').attr('class', 'alert alert-danger').text(`${word} not found on board`)
                break;
            case 'not-word':
                $('#check-word-result').attr('class', 'alert alert-danger').text(`${word} is not a word`)
                break;
            default:
                $('#check-word-result').attr('class', 'alert alert-danger').text('Unexpected Error')
        }
    }

    update_score() {
        $('#score').text(this.score)
    }

    update_time() {
        $('#time').text(this.time)
        if (this.time == 0) {
            clearInterval(this.timer)
            this.end_game()
            return
        }
        this.time--
    }

    async end_game() {
        $('#check-word-result').attr('class', 'alert alert-danger').text(`Game Over`)
        let response = await axios.post('/post-score', { score: this.score })
    }
}