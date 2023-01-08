from boggle import Boggle
from flask import Flask, render_template, session, request, jsonify


boggle_game = Boggle()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key'

@app.route('/')
def home():
    """ create and display the board """
    board =  boggle_game.make_board()
    session['board'] = board
    high_score = session.get('high_score', 0)
    total_plays = session.get('total_plays', 0)
    session['total_plays'] = total_plays
    return render_template('boggle.html', board=board, high_score=high_score, total_plays=total_plays)

@app.route('/check-word', methods=['POST'])
def check_word():
    """ checks if a word is valid """
    word = request.json.get('word')
    result = boggle_game.check_valid_word(session['board'], word)
    return jsonify({'result': result})

@app.route('/post-score', methods=['POST'])
def post_score():
    """ post score and update total plays and high score """
    high_score = session.get('high_score', 0)
    score = request.json.get('score')
    if score > high_score:
        session['high_score'] = score
    total_plays = session['total_plays']
    session['total_plays'] = total_plays + 1
    return 'OK', 200