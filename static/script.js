document.addEventListener('DOMContentLoaded', () => {
    const cells = document.querySelectorAll('.cell');
    const statusDisplay = document.getElementById('status');
    const resetButton = document.getElementById('reset-button');
    const fireworksContainer = document.getElementById('fireworks-container');
    let fireworks = null; // Initialize fireworks variable

    if (fireworksContainer) {
        fireworks = new Fireworks.default(fireworksContainer, {
            rocketsPoint: {
                min: 0,
                max: 100
            },
            hue: {
                min: 0,
                max: 360
            },
            delay: {
                min: 15,
                max: 30
            },
            speed: 2,
            acceleration: 1.05,
            friction: 0.97,
            gravity: 1.5,
            particles: 75, // Number of particles per firework
            trace: 3,
            explosion: 5,
            autoresize: true,
            brightness: {
                min: 50,
                max: 80,
                decay: {
                    min: 0.015,
                    max: 0.03
                }
            },
            sound: { // Optional: if you want sound
                enabled: false,
                // files: [
                //  'https://fireworks.js.org/sounds/explosion0.mp3',
                //  'https://fireworks.js.org/sounds/explosion1.mp3',
                //  'https://fireworks.js.org/sounds/explosion2.mp3'
                // ],
                // volume: { min: 4, max: 8 }
            }
        });
    } else {
        console.error('Fireworks container not found!');
    }

    cells.forEach(cell => {
        cell.addEventListener('click', handleCellClick);
    });

    resetButton.addEventListener('click', resetGame);

    function handleCellClick(event) {
        const row = event.target.dataset.row;
        const col = event.target.dataset.col;

        fetch('/move', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ row: parseInt(row), col: parseInt(col) }),
        })
        .then(response => response.json())
        .then(data => {
            updateBoard(data.board);
            statusDisplay.textContent = data.message;
            if (data.winner) {
                disableBoard();
                if (fireworks) {
                    fireworks.start();
                    setTimeout(() => {
                        if (fireworks) fireworks.stop();
                    }, 5000);
                }
            } else if (data.draw) {
                disableBoard();
            }
        })
        .catch(error => {
            console.error('Error:', error);
            statusDisplay.textContent = 'Error making move. See console.';
        });
    }

    function resetGame() {
        fetch('/reset', {
            method: 'POST',
        })
        .then(response => response.json())
        .then(data => {
            updateBoard(data.board);
            statusDisplay.textContent = data.message;
            enableBoard();
            if (fireworks && fireworks.running) {
                fireworks.stop();
            }
        })
        .catch(error => {
            console.error('Error:', error);
            statusDisplay.textContent = 'Error resetting game. See console.';
        });
    }

    function updateBoard(board) {
        cells.forEach(cell => {
            const r = parseInt(cell.dataset.row);
            const c = parseInt(cell.dataset.col);
            cell.textContent = board[r][c];
            cell.classList.remove('X', 'O'); // Clear previous player classes
            if (board[r][c] === 'X') {
                cell.classList.add('X');
            } else if (board[r][c] === 'O') {
                cell.classList.add('O');
            }
        });
    }

    function disableBoard() {
        cells.forEach(cell => {
            cell.removeEventListener('click', handleCellClick);
            cell.style.cursor = 'not-allowed';
        });
    }

    function enableBoard() {
        cells.forEach(cell => {
            cell.addEventListener('click', handleCellClick);
            cell.style.cursor = 'pointer';
        });
    }

    // Initial board setup (in case of page refresh and game was in progress, though app.py resets it)
    // Fetch current game state or rely on Flask template to render initial state.
    // For simplicity here, we assume initial state comes from Flask.
});