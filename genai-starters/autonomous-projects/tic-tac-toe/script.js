const board = document.querySelector('.board');
const cells = document.querySelectorAll('.cell');
let currentPlayer = 'X';
let boardState = ['', '', '', '', '', '', '', '', ''];

cells.forEach(cell => {
    cell.addEventListener('click', handleClick, { once: true });
});

function handleClick(e) {
    const cell = e.target;
    const cellIndex = cell.getAttribute('data-index');
    
    if (boardState[cellIndex] === '') {
        boardState[cellIndex] = currentPlayer;
        cell.textContent = currentPlayer;
        
        if (checkWin()) {
            setTimeout(() => alert(`${currentPlayer} wins!`), 100);
        } else if (boardState.includes('')) {
            currentPlayer = currentPlayer === 'X' ? 'O' : 'X';
        } else {
            setTimeout(() => alert('Draw!'), 100);
        }
    }
}

function checkWin() {
    const winPatterns = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ];
    return winPatterns.some(pattern => {
        return pattern.every(index => boardState[index] === currentPlayer);
    });
}