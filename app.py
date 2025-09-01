from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

class TicTacToe:
    def __init__(self):
        self.board = ['' for _ in range(9)]
        self.current_player = 'X'
        self.game_over = False
        self.winner = None
    
    def make_move(self, position):
        if self.board[position] == '' and not self.game_over:
            self.board[position] = self.current_player
            
            if self.check_winner():
                self.winner = self.current_player
                self.game_over = True
            elif '' not in self.board:
                self.game_over = True
                self.winner = 'Tie'
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
            
            return True
        return False
    
    def check_winner(self):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
            [0, 4, 8], [2, 4, 6]              # diagonals
        ]
        
        for combo in winning_combinations:
            if (self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != ''):
                return True
        return False
    
    def reset(self):
        self.board = ['' for _ in range(9)]
        self.current_player = 'X'
        self.game_over = False
        self.winner = None
    
    def get_state(self):
        return {
            'board': self.board,
            'current_player': self.current_player,
            'game_over': self.game_over,
            'winner': self.winner
        }

game = TicTacToe()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/move', methods=['POST'])
def make_move():
    data = request.json
    position = data.get('position')
    
    if position is not None and 0 <= position <= 8:
        success = game.make_move(position)
        return jsonify({'success': success, 'game_state': game.get_state()})
    
    return jsonify({'success': False, 'error': 'Invalid position'})

@app.route('/reset', methods=['POST'])
def reset_game():
    game.reset()
    return jsonify({'success': True, 'game_state': game.get_state()})

@app.route('/state')
def get_state():
    return jsonify(game.get_state())

if __name__ == '__main__':
    app.run(debug=True)