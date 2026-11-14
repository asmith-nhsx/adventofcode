// Noughts and Crosses (tic-tac-toe) in plain JavaScript.

const WIN_LINES = [
  [0, 1, 2], [3, 4, 5], [6, 7, 8], // rows
  [0, 3, 6], [1, 4, 7], [2, 5, 8], // columns
  [0, 4, 8], [2, 4, 6],            // diagonals
];

const boardEl = document.getElementById('board');
const statusEl = document.getElementById('status');
const scoreEls = {
  X: document.getElementById('score-x'),
  O: document.getElementById('score-o'),
  draw: document.getElementById('score-draw'),
};

let board;          // array of 9: 'X', 'O' or null
let current;        // whose turn: 'X' or 'O'
let gameOver;
const scores = { X: 0, O: 0, draw: 0 };

// Build the 9 cells once.
const cells = [];
for (let i = 0; i < 9; i++) {
  const btn = document.createElement('button');
  btn.className = 'cell';
  btn.setAttribute('aria-label', `Cell ${i + 1}`);
  btn.addEventListener('click', () => handleMove(i));
  boardEl.appendChild(btn);
  cells.push(btn);
}

function vsComputer() {
  return document.querySelector('input[name="mode"]:checked').value === 'cpu';
}

function newGame() {
  board = Array(9).fill(null);
  current = 'X';
  gameOver = false;
  cells.forEach(c => {
    c.textContent = '';
    c.className = 'cell';
    c.disabled = false;
  });
  statusEl.textContent = 'X to play';
}

function findWinner(b) {
  for (const line of WIN_LINES) {
    const [a, c, d] = line;
    if (b[a] && b[a] === b[c] && b[a] === b[d]) {
      return { player: b[a], line };
    }
  }
  return null;
}

function handleMove(i) {
  if (gameOver || board[i]) return;
  placeMark(i);

  // Computer plays O.
  if (!gameOver && vsComputer() && current === 'O') {
    setBoardEnabled(false);
    setTimeout(() => {
      placeMark(computerMove());
      if (!gameOver) setBoardEnabled(true);
    }, 300);
  }
}

function placeMark(i) {
  board[i] = current;
  cells[i].textContent = current;
  cells[i].classList.add(current.toLowerCase());
  cells[i].disabled = true;

  const win = findWinner(board);
  if (win) {
    win.line.forEach(idx => cells[idx].classList.add('win'));
    endGame(`${win.player} wins!`, win.player);
  } else if (board.every(Boolean)) {
    endGame("It's a draw!", 'draw');
  } else {
    current = current === 'X' ? 'O' : 'X';
    statusEl.textContent = `${current} to play`;
  }
}

function endGame(message, result) {
  gameOver = true;
  statusEl.textContent = message;
  scores[result]++;
  scoreEls[result].textContent = scores[result];
  setBoardEnabled(false);
}

function setBoardEnabled(enabled) {
  cells.forEach((c, i) => {
    c.disabled = !enabled || board[i] !== null;
  });
}

// Simple computer: win if possible, block if needed,
// otherwise take centre, then a corner, then any free cell.
function computerMove() {
  const free = board.map((v, i) => (v ? null : i)).filter(i => i !== null);

  for (const player of ['O', 'X']) {   // try to win first, then block
    for (const i of free) {
      const trial = board.slice();
      trial[i] = player;
      if (findWinner(trial)) return i;
    }
  }

  if (free.includes(4)) return 4;
  const corners = [0, 2, 6, 8].filter(i => free.includes(i));
  const options = corners.length ? corners : free;
  return options[Math.floor(Math.random() * options.length)];
}

document.getElementById('new-game').addEventListener('click', newGame);
document.getElementById('reset-scores').addEventListener('click', () => {
  scores.X = scores.O = scores.draw = 0;
  Object.keys(scoreEls).forEach(k => (scoreEls[k].textContent = '0'));
});
document.querySelectorAll('input[name="mode"]').forEach(r =>
  r.addEventListener('change', newGame)
);

newGame();
