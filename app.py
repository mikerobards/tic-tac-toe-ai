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
    
    def get_available_moves(self):
        return [i for i, cell in enumerate(self.board) if cell == '']
    
    def evaluate_board(self):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        
        for combo in winning_combinations:
            if (self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != ''):
                if self.board[combo[0]] == 'O':
                    return 10
                else:
                    return -10
        
        if '' not in self.board:
            return 0
        
        return None
    
    def minimax(self, depth, is_maximizing):
        score = self.evaluate_board()
        
        if score is not None:
            if score == 10:
                return score - depth
            elif score == -10:
                return score + depth
            else:
                return score
        
        if is_maximizing:
            best_score = float('-inf')
            for move in self.get_available_moves():
                self.board[move] = 'O'
                current_score = self.minimax(depth + 1, False)
                self.board[move] = ''
                best_score = max(best_score, current_score)
            return best_score
        else:
            best_score = float('inf')
            for move in self.get_available_moves():
                self.board[move] = 'X'
                current_score = self.minimax(depth + 1, True)
                self.board[move] = ''
                best_score = min(best_score, current_score)
            return best_score
    
    def ai_move(self):
        if self.game_over or self.current_player != 'O':
            return None
            
        available_moves = self.get_available_moves()
        if not available_moves:
            return None
        
        # AI strategy: try to win, block opponent, take center, take corners, take edges
        best_move = self.find_best_move()
        if best_move is not None:
            self.make_move(best_move)
            return best_move
        
        return None
    
    def find_best_move(self):
        best_move = None
        best_score = float('-inf')
        
        for move in self.get_available_moves():
            self.board[move] = 'O'
            score = self.minimax(0, False)
            self.board[move] = ''
            
            if score > best_score:
                best_score = score
                best_move = move
        
        return best_move

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
        # Only allow human moves when it's X's turn
        if game.current_player != 'X':
            return jsonify({'success': False, 'error': 'Not your turn'})
        
        # Make human move
        success = game.make_move(position)
        if not success:
            return jsonify({'success': False, 'error': 'Invalid move'})
        
        # If game is not over and it's AI's turn, make AI move
        if not game.game_over and game.current_player == 'O':
            game.ai_move()
        
        return jsonify({'success': True, 'game_state': game.get_state()})
    
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