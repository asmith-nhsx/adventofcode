// 3D Noughts and Crosses (3x3x3) in plain JavaScript.
// The cube is shown as three flat 3x3 layers.
// Cell index = layer * 9 + row * 3 + col.

const SIZE = 3;
const CELLS = SIZE * SIZE * SIZE; // 27

const idx = (x, y, z) => z * 9 + y * 3 + x;

// The very centre of the cube (middle square of the middle layer) is
// banned: it sits on 13 lines and taking it gives X a forced win.
const BANNED = idx(1, 1, 1); // 13
const BLOCKED = '#';         // board value for the banned cell

// Build every winning line: for each start cell and each of the 26
// directions, keep the line if all 3 cells fit inside the cube.
// Each line is found from both ends, so de-duplicate. That gives 49
// lines; dropping the 13 through the banned centre leaves 36.
const WIN_LINES = (() => {
  const seen = new Set();
  const lines = [];
  for (let z = 0; z < SIZE; z++)
    for (let y = 0; y < SIZE; y++)
      for (let x = 0; x < SIZE; x++)
        for (let dz = -1; dz <= 1; dz++)
          for (let dy = -1; dy <= 1; dy++)
            for (let dx = -1; dx <= 1; dx++) {
              if (!dx && !dy && !dz) continue;
              const line = [];
              for (let s = 0; s < SIZE; s++) {
                const nx = x + dx * s, ny = y + dy * s, nz = z + dz * s;
                if (nx < 0 || ny < 0 || nz < 0 || nx >= SIZE || ny >= SIZE || nz >= SIZE) break;
                line.push(idx(nx, ny, nz));
              }
              if (line.length !== SIZE) continue;
              const key = line.slice().sort((a, b) => a - b).join(',');
              if (!seen.has(key)) {
                seen.add(key);
                lines.push(line);
              }
            }
  return lines.filter(l => !l.includes(BANNED));
})();

// Lines passing through each cell (used for move ordering).
const LINES_THROUGH = Array.from({ length: CELLS }, (_, i) =>
  WIN_LINES.filter(l => l.includes(i)).length
);

const boardsEl = document.getElementById('boards');
const statusEl = document.getElementById('status');
const scoreEls = {
  X: document.getElementById('score-x'),
  O: document.getElementById('score-o'),
  draw: document.getElementById('score-draw'),
};

let board;          // array of 27: 'X', 'O' or null
let current;        // whose turn: 'X' or 'O'
let gameOver;
const scores = { X: 0, O: 0, draw: 0 };

// Build the three layers of cells once.
const LAYER_NAMES = ['Top layer', 'Middle layer', 'Bottom layer'];
const cells = [];
for (let z = 0; z < SIZE; z++) {
  const layer = document.createElement('div');
  layer.className = 'layer';
  const title = document.createElement('h2');
  title.textContent = LAYER_NAMES[z];
  const grid = document.createElement('div');
  grid.className = 'board';
  for (let i = 0; i < 9; i++) {
    const index = z * 9 + i;
    const btn = document.createElement('button');
    btn.className = 'cell';
    btn.setAttribute('aria-label', `${LAYER_NAMES[z]}, cell ${i + 1}`);
    btn.addEventListener('click', () => handleMove(index));
    grid.appendChild(btn);
    cells[index] = btn;
  }
  layer.append(title, grid);
  boardsEl.appendChild(layer);
}

function vsComputer() {
  return document.querySelector('input[name="mode"]:checked').value === 'cpu';
}

function newGame() {
  board = Array(CELLS).fill(null);
  current = 'X';
  gameOver = false;
  cells.forEach(c => {
    c.textContent = '';
    c.className = 'cell';
    c.disabled = false;
  });
  board[BANNED] = BLOCKED;
  cells[BANNED].classList.add('blocked');
  cells[BANNED].disabled = true;
  cells[BANNED].setAttribute('aria-label', 'Centre of the cube (not playable)');
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
    statusEl.textContent = 'Computer is thinking…';
    setTimeout(() => {
      placeMark(computerMove());
      if (!gameOver) setBoardEnabled(true);
    }, 50);
  }
}

function placeMark(i) {
  board[i] = current;
  cells[i].textContent = current;
  cells[i].classList.add(current.toLowerCase());
  cells[i].disabled = true;

  const win = findWinner(board);
  if (win) {
    win.line.forEach(k => cells[k].classList.add('win'));
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

// ---------------------------------------------------------------------------
// Computer opponent (plays O).
// A full game-tree search of 27 cells is far too big, so it uses minimax
// with alpha-beta pruning to a limited depth, then scores the position:
// each line still open to only one player is worth points to that player,
// and two-in-a-line (a threat) is worth much more than one.
// ---------------------------------------------------------------------------
const SEARCH_DEPTH = 4;
const WIN_SCORE = 100000;

function freeCells(b) {
  const free = [];
  for (let i = 0; i < CELLS; i++) if (!b[i]) free.push(i);
  // Try the most connected cells first: makes pruning far more effective.
  return free.sort((a, c) => LINES_THROUGH[c] - LINES_THROUGH[a]);
}

function evaluate(b) {
  let score = 0;
  for (const [a, c, d] of WIN_LINES) {
    let o = 0, x = 0;
    for (const v of [b[a], b[c], b[d]]) {
      if (v === 'O') o++;
      else if (v === 'X') x++;
    }
    if (o && x) continue;       // blocked line, worthless to both
    if (o === 2) score += 50;
    else if (o === 1) score += 2;
    if (x === 2) score -= 50;
    else if (x === 1) score -= 2;
  }
  return score;
}

function minimax(b, player, depth, alpha, beta) {
  const win = findWinner(b);
  if (win) return win.player === 'O' ? WIN_SCORE - depth : depth - WIN_SCORE;
  const free = freeCells(b);
  if (free.length === 0) return 0;
  if (depth >= SEARCH_DEPTH) return evaluate(b);

  if (player === 'O') {
    let best = -Infinity;
    for (const i of free) {
      b[i] = 'O';
      best = Math.max(best, minimax(b, 'X', depth + 1, alpha, beta));
      b[i] = null;
      alpha = Math.max(alpha, best);
      if (alpha >= beta) break;
    }
    return best;
  } else {
    let best = Infinity;
    for (const i of free) {
      b[i] = 'X';
      best = Math.min(best, minimax(b, 'O', depth + 1, alpha, beta));
      b[i] = null;
      beta = Math.min(beta, best);
      if (alpha >= beta) break;
    }
    return best;
  }
}

function computerMove() {
  const b = board.slice();
  let bestScore = -Infinity;
  let bestMoves = [];

  for (const i of freeCells(b)) {
    b[i] = 'O';
    const score = minimax(b, 'X', 1, -Infinity, Infinity);
    b[i] = null;
    if (score > bestScore) {
      bestScore = score;
      bestMoves = [i];
    } else if (score === bestScore) {
      bestMoves.push(i);
    }
  }

  // Pick randomly among equally good moves so games vary.
  return bestMoves[Math.floor(Math.random() * bestMoves.length)];
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
