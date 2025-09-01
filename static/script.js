class TicTacToe {
    constructor() {
        this.board = document.getElementById('game-board');
        this.cells = document.querySelectorAll('.cell');
        this.currentPlayerElement = document.getElementById('player-indicator');
        this.gameStatusElement = document.getElementById('game-status');
        this.resetButton = document.getElementById('reset-btn');
        this.modal = document.getElementById('win-modal');
        this.winMessage = document.getElementById('win-message');
        this.playAgainButton = document.getElementById('play-again-btn');
        
        this.initializeGame();
        this.addEventListeners();
    }
    
    initializeGame() {
        this.getGameState();
    }
    
    addEventListeners() {
        this.cells.forEach((cell, index) => {
            cell.addEventListener('click', () => this.makeMove(index));
        });
        
        this.resetButton.addEventListener('click', () => this.resetGame());
        this.playAgainButton.addEventListener('click', () => this.resetGame());
        
        this.modal.addEventListener('click', (e) => {
            if (e.target === this.modal) {
                this.closeModal();
            }
        });
    }
    
    async makeMove(position) {
        try {
            const response = await fetch('/move', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ position: position })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.updateGameState(data.game_state);
                this.animateMove(position, data.game_state.board[position]);
            }
        } catch (error) {
            console.error('Error making move:', error);
        }
    }
    
    async resetGame() {
        try {
            const response = await fetch('/reset', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.updateGameState(data.game_state);
                this.closeModal();
                this.clearAnimations();
            }
        } catch (error) {
            console.error('Error resetting game:', error);
        }
    }
    
    async getGameState() {
        try {
            const response = await fetch('/state');
            const gameState = await response.json();
            this.updateGameState(gameState);
        } catch (error) {
            console.error('Error getting game state:', error);
        }
    }
    
    updateGameState(gameState) {
        this.cells.forEach((cell, index) => {
            const value = gameState.board[index];
            cell.textContent = value;
            cell.className = 'cell';
            
            if (value) {
                cell.classList.add(value.toLowerCase());
            }
        });
        
        this.currentPlayerElement.textContent = gameState.current_player;
        this.currentPlayerElement.className = '';
        this.currentPlayerElement.classList.add(gameState.current_player.toLowerCase());
        
        if (gameState.game_over) {
            this.handleGameEnd(gameState.winner);
        } else {
            this.gameStatusElement.textContent = `${gameState.current_player}'s turn`;
        }
        
        this.updateCellStates(gameState.game_over);
    }
    
    updateCellStates(gameOver) {
        this.cells.forEach(cell => {
            if (gameOver || cell.textContent !== '') {
                cell.style.pointerEvents = 'none';
            } else {
                cell.style.pointerEvents = 'auto';
            }
        });
    }
    
    handleGameEnd(winner) {
        let message;
        if (winner === 'Tie') {
            message = "It's a Tie!";
            this.gameStatusElement.textContent = "Game ended in a tie";
        } else {
            message = `${winner} Wins!`;
            this.gameStatusElement.textContent = `${winner} is the winner!`;
        }
        
        this.winMessage.textContent = message;
        
        setTimeout(() => {
            this.showModal();
        }, 1000);
    }
    
    animateMove(position, player) {
        const cell = this.cells[position];
        cell.classList.add('cell-animation');
        
        setTimeout(() => {
            cell.classList.remove('cell-animation');
        }, 300);
    }
    
    clearAnimations() {
        this.cells.forEach(cell => {
            cell.classList.remove('cell-animation');
        });
    }
    
    showModal() {
        this.modal.style.display = 'block';
        document.body.style.overflow = 'hidden';
    }
    
    closeModal() {
        this.modal.style.display = 'none';
        document.body.style.overflow = 'auto';
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new TicTacToe();
});