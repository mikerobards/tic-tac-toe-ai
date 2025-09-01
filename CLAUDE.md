# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Development

- **Run the application**: `python app.py` (starts Flask development server on <http://localhost:5000>)
- **Install dependencies**: `pip install -r requirements.txt`

## Architecture

This is a web-based tic-tac-toe game with AI opponent built with Flask and vanilla JavaScript:

### Backend (Flask)

- **app.py**: Main Flask application with a `TicTacToe` class that manages game state and AI logic
- Game logic handles moves, win detection, and state management
- **AI Implementation**: Uses minimax algorithm with alpha-beta pruning for optimal AI moves
  - `minimax()`: Recursive algorithm that evaluates all possible game states
  - `evaluate_board()`: Scores board positions (+10 for AI win, -10 for player win, 0 for tie)
  - `find_best_move()`: Determines optimal AI move using minimax
  - `ai_move()`: Executes AI turn automatically after player move
- REST API endpoints:
  - `POST /move` - Make a human move (X), triggers AI response (O) if game continues
  - `POST /reset` - Reset the game
  - `GET /state` - Get current game state

### Frontend

- **templates/index.html**: Single HTML template with game board and modal
- **static/script.js**: `TicTacToe` class that handles DOM manipulation and API communication
- **static/style.css**: Game styling with animations and player-specific styling

### Game Flow

1. Frontend `TicTacToe` class initializes and fetches game state
2. Player (X) clicks trigger moves via POST requests to `/move`
3. Backend processes human move and automatically executes AI move (O) if game continues
4. Frontend updates UI with animations and handles game end states
5. Modal appears for game results with play again option
6. AI provides optimal gameplay using minimax algorithm

### AI Features

- **Player vs AI**: Human always plays as X, AI plays as O
- **Minimax Algorithm**: AI uses perfect play strategy, never loses (wins or draws)
- **Automatic Turns**: AI moves immediately after valid human moves
- **Smart UI**: Shows "AI thinking..." during AI turn processing
