# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Development
- **Run the application**: `python app.py` (starts Flask development server on http://localhost:5000)
- **Install dependencies**: `pip install -r requirements.txt`

## Architecture

This is a web-based tic-tac-toe game built with Flask and vanilla JavaScript:

### Backend (Flask)
- **app.py**: Main Flask application with a `TicTacToe` class that manages game state
- Game logic handles moves, win detection, and state management
- REST API endpoints:
  - `POST /move` - Make a move at a specific position
  - `POST /reset` - Reset the game
  - `GET /state` - Get current game state

### Frontend
- **templates/index.html**: Single HTML template with game board and modal
- **static/script.js**: `TicTacToe` class that handles DOM manipulation and API communication
- **static/style.css**: Game styling (not analyzed but present)

### Game Flow
1. Frontend `TicTacToe` class initializes and fetches game state
2. Player clicks trigger moves via POST requests to `/move`
3. Backend updates game state and returns new state
4. Frontend updates UI with animations and handles game end states
5. Modal appears for game results with play again option

The game uses a single global game instance on the backend, so all players share the same game state.