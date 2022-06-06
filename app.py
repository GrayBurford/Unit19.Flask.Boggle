from boggle import Boggle
from flask import Flask, session, request, render_template, jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = 'abc123'

boggle_game = Boggle()

@app.route('/')
def home():
    """Generate gameboard, add it to session, define highscore and times played, and pass them all into template to be rendered."""
    
    board = boggle_game.make_board() # generates a list matrix with random letters
    session['board'] = board # adds this specific board set to session
    # get highscore and times played from session, otherwise set default to 0
    highscore = session.get('highscore', 0)
    times_played = session.get('times_played', 0)
    return render_template('index.html', board = board, highscore = highscore, times_played = times_played) # render home template to generate td's for each board element. Must pass board through.

@app.route('/check-word')
def check_word_validity():
    """Take word from params from axios GET request and check it against our board"""
    word = request.args['word']
    board = session['board']
    response = boggle_game.check_valid_word(board, word)
    return jsonify({'result' : response})

@app.route('/game-over', methods=["POST"])
def run_game_over():
    """Receive axios post request from gameOver function, and update highscore and times played in session"""
    print(request.json)
    print("Game over from /game-over")

    currScore = request.json['currScore']
    highscore = session.get('highscore', 0)
    times_played = session.get('times_played', 0)

    if currScore > highscore:
        session['highscore'] = currScore

    session['times_played'] = times_played + 1;

    return ""