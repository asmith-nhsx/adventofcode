// 3D Noughts and Crosses (3x3x3) in plain JavaScript.
// The cube is shown as three flat 3x3 layers.
// Cell index = layer * 9 + row * 3 + col.
//
// Play continues after a line is made: the first player to complete
// LINES_TO_WIN lines wins. If the board fills first, most lines wins.

const SIZE = 3;
const CELLS = SIZE * SIZE * SIZE; // 27
const LINES_TO_WIN = 3;

const idx = (x, y, z) => z * 9 + y * 3 + x;

// The very centre of the cube (middle square of the middle layer) is
// banned: it sits on 13 lines and taking it gives X a huge advantage.
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
const resultEl = document.getElementById('result');
const resultTextEl = document.getElementById('result-text');
const scoreEls = {
  X: document.getElementById('score-x'),
  O: document.getElementById('score-o'),
  draw: document.getElementById('score-draw'),
};

let board;          // array of 27: 'X', 'O', BLOCKED or null
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

// The rotatable 3D board (view3d.js). If three.js fails to load, for
// example when offline, the flat layer boards still work on their own.
const view3dEl = document.getElementById('view3d');
let view = null;
try {
  view = createView3D(view3dEl, handleMove);
} catch (err) {
  console.warn('3D view unavailable, using flat boards only:', err);
  view3dEl.hidden = true;
}

function vsComputer() {
  return document.querySelector('input[name="mode"]:checked').value === 'cpu';
}

function newGame() {
  board = Array(CELLS).fill(null);
  current = 'X';
  gameOver = false;
  resultEl.hidden = true;
  boardsEl.classList.remove('game-over');
  cells.forEach(c => {
    c.textContent = '';
    c.className = 'cell';
    c.disabled = false;
  });
  board[BANNED] = BLOCKED;
  cells[BANNED].classList.add('blocked');
  cells[BANNED].disabled = true;
  cells[BANNED].setAttribute('aria-label', 'Centre of the cube (not playable)');
  if (view) {
    view.reset(BANNED);
    view.setTurn(current);
    view.setInteractive(true);
  }
  updateStatus(countLines(board));
}

// Completed lines for each player.
function completedLines(b) {
  const done = { X: [], O: [] };
  for (const line of WIN_LINES) {
    const [a, c, d] = line;
    if ((b[a] === 'X' || b[a] === 'O') && b[a] === b[c] && b[a] === b[d]) {
      done[b[a]].push(line);
    }
  }
  return done;
}

function countLines(b) {
  const done = completedLines(b);
  return { X: done.X.length, O: done.O.length };
}

const plural = n => `${n} line${n === 1 ? '' : 's'}`;

function updateStatus(counts, prefix = `${current} to play`) {
  statusEl.textContent =
    `${prefix} · X: ${plural(counts.X)}, O: ${plural(counts.O)} (first to ${LINES_TO_WIN})`;
}

function handleMove(i) {
  if (gameOver || board[i]) return;
  if (vsComputer() && current === 'O') return;  // computer's turn
  placeMark(i);

  // Computer plays O.
  if (!gameOver && vsComputer() && current === 'O') {
    setBoardEnabled(false);
    updateStatus(countLines(board), 'Computer is thinking…');
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

  // Highlight every completed line (a move can complete several at once).
  const done = completedLines(board);
  for (const line of [...done.X, ...done.O]) {
    line.forEach(k => cells[k].classList.add('win'));
  }
  const counts = { X: done.X.length, O: done.O.length };
  if (view) {
    view.setMark(i, current);
    view.showLines(done);
  }

  if (counts[current] >= LINES_TO_WIN) {
    endGame(`${current} wins!`, current, counts);
  } else if (board.every(Boolean)) {
    // Board full before anyone reached the target: most lines wins.
    if (counts.X === counts.O) endGame("Board full: it's a draw!", 'draw', counts);
    else {
      const leader = counts.X > counts.O ? 'X' : 'O';
      endGame(`Board full: ${leader} wins on lines!`, leader, counts);
    }
  } else {
    current = current === 'X' ? 'O' : 'X';
    if (view) view.setTurn(current);
    updateStatus(counts);
  }
}

function endGame(message, result, counts) {
  gameOver = true;
  updateStatus(counts, message);
  scores[result]++;
  scoreEls[result].textContent = scores[result];
  setBoardEnabled(false);

  // Big coloured banner, and fade everything except the completed lines.
  let text = message;
  if (vsComputer() && result !== 'draw') {
    text = result === 'X' ? '🎉 You win!' : 'Computer wins!';
  }
  resultTextEl.textContent = text;
  resultEl.className = `result ${result.toLowerCase()}`;
  resultEl.hidden = false;
  boardsEl.classList.add('game-over');
  if (view) view.setGameOver(completedLines(board));
  document.getElementById('play-again').focus();
}

function setBoardEnabled(enabled) {
  cells.forEach((c, i) => {
    c.disabled = !enabled || board[i] !== null;
  });
  if (view) view.setInteractive(enabled);
}

// ---------------------------------------------------------------------------
// Computer opponent (plays O).
// Minimax with alpha-beta pruning to a limited depth. Positions are scored by
// completed lines (heavily weighted), then by lines still open to only one
// player, with two-in-a-line (a threat) worth much more than one.
// ---------------------------------------------------------------------------
const SEARCH_DEPTH = 4;
const WIN_SCORE = 1000000;
const LINE_SCORE = 1000;

function freeCells(b) {
  const free = [];
  for (let i = 0; i < CELLS; i++) if (!b[i]) free.push(i);
  // Try the most connected cells first: makes pruning far more effective.
  return free.sort((a, c) => LINES_THROUGH[c] - LINES_THROUGH[a]);
}

// One pass over the lines: completed counts plus a positional score.
function analyse(b) {
  let x3 = 0, o3 = 0, score = 0;
  for (const [a, c, d] of WIN_LINES) {
    let o = 0, x = 0;
    for (const v of [b[a], b[c], b[d]]) {
      if (v === 'O') o++;
      else if (v === 'X') x++;
    }
    if (o === 3) o3++;
    else if (x === 3) x3++;
    else if (o && x) continue;  // blocked line, worthless to both
    else if (o === 2) score += 50;
    else if (o === 1) score += 2;
    else if (x === 2) score -= 50;
    else if (x === 1) score -= 2;
  }
  return { x3, o3, score: score + (o3 - x3) * LINE_SCORE };
}

function minimax(b, player, depth, alpha, beta) {
  const { x3, o3, score } = analyse(b);
  if (o3 >= LINES_TO_WIN) return WIN_SCORE - depth;
  if (x3 >= LINES_TO_WIN) return depth - WIN_SCORE;
  const free = freeCells(b);
  if (free.length === 0) {
    if (o3 === x3) return 0;
    return o3 > x3 ? WIN_SCORE - depth : depth - WIN_SCORE;
  }
  if (depth >= SEARCH_DEPTH) return score;

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
document.getElementById('play-again').addEventListener('click', newGame);
document.getElementById('reset-scores').addEventListener('click', () => {
  scores.X = scores.O = scores.draw = 0;
  Object.keys(scoreEls).forEach(k => (scoreEls[k].textContent = '0'));
});
document.querySelectorAll('input[name="mode"]').forEach(r =>
  r.addEventListener('change', newGame)
);

newGame();
