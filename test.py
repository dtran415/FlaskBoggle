from unittest import TestCase
from app import app
from flask import session, json
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):
        """Set up test client"""

        self.client = app.test_client()
        app.config['TESTING'] = True
        self.board = [['C', 'N', 'N', 'A', 'L'],
                      ['H', 'M', 'T', 'K', 'G'],
                      ['M', 'S', 'H', 'N', 'G'],
                      ['A', 'F', 'N', 'V', 'P'],
                      ['D', 'H', 'K', 'T', 'U']]
        self.boggle = Boggle()

    def test_home(self):
        """ check home page for elements """
        with self.client as client:
            response = client.get('/')
            self.assertIn('board', session)
            self.assertIsNone(session.get('highscore'))
            self.assertEqual(session.get('total_plays'), 0)
            self.assertIn(b'Score:', response.data)
            self.assertIn(b'High Score:', response.data)
            self.assertIn(b'Total Plays:', response.data)
            self.assertIn(b'Time:', response.data)

    def test_check_word_valid_word(self):
        """ check if valid word returns ok """

        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = self.board

            post_data = {'word': 'mad'}
            response = client.post(
                '/check-word', data=json.dumps(post_data), content_type='application/json')
            self.assertEqual(response.json['result'], 'ok')
            post_data = {'word': 'nag'}
            response = client.post(
                '/check-word', data=json.dumps(post_data), content_type='application/json')
            self.assertEqual(response.json['result'], 'ok')

    def test_check_word_word_not_on_board(self):
        """ check if valid word but not on board returns not-on-board """

        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = self.board

            post_data = {'word': 'dog'}
            response = client.post(
                '/check-word', data=json.dumps(post_data), content_type='application/json')
            self.assertEqual(response.json['result'], 'not-on-board')

    def test_check_word_invalid_word(self):
        """ check if invalid word returns not-word """

        with self.client as client:
            with client.session_transaction() as session:
                session['board'] = self.board
            post_data = {'word': 'lksdajfadslfj'}
            response = client.post(
                '/check-word', data=json.dumps(post_data), content_type='application/json')
            self.assertEqual(response.json['result'], 'not-word')

    def test_check_word_missing_word(self):
        """ check if missing word gives a 400 """

        with self.client as client:
            response = client.post(
                '/check-word', content_type='application/json')
            self.assertEqual(response.status_code, 400)

    def test_post_score(self):
        """ check if high score gets updated if score greater than current high """

        with self.client as client:
            post_data = {'score': 10}
            response = client.get('/')
            response = client.post(
                '/post-score', data=json.dumps(post_data), content_type='application/json')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(session['high_score'], 10)
            self.assertEqual(session['total_plays'], 1)
            post_data = {'score': 1}
            response = client.post(
                '/post-score', data=json.dumps(post_data), content_type='application/json')
            self.assertEqual(session['high_score'], 10)
            self.assertEqual(session['total_plays'], 2)

    def test_post_score_missing_score(self):
        """ check if missing score returns 400 """
        with self.client as client:
            response = client.post(
                '/post-score', content_type='application/json')
            self.assertEqual(response.status_code, 400)

    def test_read_dict(self):
        """ check to see if words get loaded properly """
        self.assertGreater(len(self.boggle.words), 0)

    def test_make_board(self):
        """ check to see if a 5x5 board is created """
        board = self.boggle.make_board()
        self.assertEqual(len(board), 5)
        self.assertEqual(len(board[0]), 5)

    def test_check_valid_word(self):
        result = self.boggle.check_valid_word(self.board, 'mad')
        self.assertEqual(result, 'ok')
        result = self.boggle.check_valid_word(self.board, 'cat')
        self.assertEqual(result, 'not-on-board')
        result = self.boggle.check_valid_word(self.board, 'knerkoj')
        self.assertEqual(result, 'not-word')

    def test_find(self):
        result = self.boggle.find(self.board, 'MAD')
        self.assertTrue(result)
        result = self.boggle.find(self.board, 'CAT')
        self.assertFalse(result)
