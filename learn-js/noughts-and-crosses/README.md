# Learning JavaScript: Noughts and Crosses

A step-by-step project for learning JavaScript by building a noughts and crosses
game with plain HTML, CSS and JavaScript (no frameworks). This file is updated
as each step is completed.

## How to run it

Open `index.html` in a browser (double-click it, or right-click → *Open with
Live Server* in VS Code). Press **F12** and open the **Console** tab to see
messages from `console.log`.

## Files

| File         | Purpose                                  |
|--------------|------------------------------------------|
| `index.html` | The page: the board, status text, restart button |
| `style.css`  | Layout and styling                       |
| `script.js`  | All the game logic                       |

## Progress

- [x] Step 1: Page structure
- [x] Step 2: Make clicks do something
- [x] Step 3: Store the board in an array and take turns between X and O
- [x] Step 4: Check for a win or a draw
- [ ] Step 5: Restart button

---

## Step 1: Page structure ✅

Set up `index.html`, `style.css` and a `script.js` that logs
`script.js is loaded!` to the console to prove it is connected.

Things to notice in the HTML:

- **Each square is a `<button>`**, so it is clickable and works with the
  keyboard without extra code. That's a good habit for accessibility.
- **`data-index="0"` to `"8"`** numbers the squares so JavaScript can tell which
  one was clicked:

  ```
  0 | 1 | 2
  3 | 4 | 5
  6 | 7 | 8
  ```

- **`<script>` is at the bottom of `<body>`.** The browser reads the page top to
  bottom, so the board has to exist before the script tries to find it.

**Key idea:** the board on screen only *displays* the game, it isn't where the
game is stored. In JavaScript we keep an array of 9 values as the "real" board,
and update the screen to match it.

## Step 2: Make clicks do something ✅

What I wrote:

```js
const cells = document.querySelectorAll(".cell");
cells.forEach((cell) => {
  cell.addEventListener("click", (event) => {
    console.log(`Cell clicked ${event.target.dataset.index}`);
  });
});
```

Clicking a square logs e.g. `Cell clicked 4`.

### What I learned

**`querySelectorAll` + `forEach`** finds every element matching a CSS selector
and loops over them to attach the same handler to each one.

**Template literals** use backticks, with `${ }` for variables or any
expression:

```js
console.log(`You clicked square ${index}`);
console.log(`Next square is ${index + 1}`);
```

Normal `"quotes"` don't substitute: `"Square ${index}"` prints that text
literally. `console.log("Board:", board)` (with a comma) is better for objects
and arrays, because DevTools shows them as expandable trees.

**The event object.** The browser calls the handler and passes it an event
object describing what happened:

| Property | What it is |
|---|---|
| `event.target` | The element that was actually clicked |
| `event.currentTarget` | The element the listener is attached to |
| `event.type` | The kind of event, e.g. `"click"` |
| `event.clientX` / `clientY` | Mouse position in the window |

Tip: `console.log(event)` and expand it in DevTools to explore it.

**`dataset`.** Any `data-something` attribute in the HTML can be read as
`element.dataset.something`. It is always a **string** (`"4"`), so use
`Number(...)` to turn it into a number.

**Closures.** Inside the handler, `cell` from the surrounding loop is still
available, so `cell.dataset.index` works as well as
`event.target.dataset.index`. Functions "remember" the variables around them.

## Step 3: Store the board and take turns ✅

What I wrote:

```js
let board = ["", "", "", "", "", "", "", "", ""];
let currentPlayer = "X";

const cells = document.querySelectorAll(".cell");
const statusMsg = document.getElementById("status");

cells.forEach((cell) => {
  cell.addEventListener("click", (event) => {
    let index = parseInt(event.target.dataset.index);
    if (board[index] === "") {
      board[index] = currentPlayer;
      event.target.textContent = currentPlayer;
      currentPlayer = currentPlayer === "X" ? "O" : "X";
      statusMsg.textContent = `Current player: ${currentPlayer}`;
    }
  });
});
```

### What I learned

- **Game state lives in JavaScript, not the page.** `board` is the source of
  truth; the buttons just display it.
- **`===` (strict equality)** compares without converting types. Prefer it to
  `==`, where `0 == ""` is `true`.
- **Ternary operator:** `condition ? valueIfTrue : valueIfFalse`, e.g.
  `currentPlayer = currentPlayer === "X" ? "O" : "X";`
- **Look up elements once** (outside the loop or handler) and reuse them.
- **`const` by default, `let` only if the variable is reassigned.**
- **`parseInt` vs `Number`:** `parseInt("4abc")` is `4`; `Number("4abc")` is
  `NaN`. With `parseInt`, pass the base: `parseInt(value, 10)`.
- **Guard clauses** exit early instead of nesting:

  ```js
  if (board[index] !== "") return; // square taken: ignore the click
  ```

## Step 4: Check for a win or a draw ✅

What I wrote (key parts):

```js
const winningLines = [
  [0, 1, 2], [3, 4, 5], [6, 7, 8], // rows
  [0, 3, 6], [1, 4, 7], [2, 5, 8], // columns
  [0, 4, 8], [2, 4, 6],            // diagonals
];
let gameOver = false;

function checkWinner() {
  for (const [a, b, c] of winningLines) {
    if (board[a] !== "" && board[a] === board[b] && board[b] === board[c]) {
      return board[a];
    }
  }
  return null;
}

// inside the click handler, after placing the move:
if (gameOver) return;
// ...
const winner = checkWinner();
if (winner !== null) {
  gameOver = true;
  statusMsg.textContent = `Player ${winner} wins!`;
  return;
}
if (!board.includes("")) {
  gameOver = true;
  statusMsg.textContent = "It's a draw!";
  return;
}
```

### What I learned

**Destructuring** unpacks arrays/objects into variables in one line.

```js
const [first, second, third] = ["red", "green", "blue"]; // by position
const [a, , c] = [1, 2, 3];        // skip one
const [head, ...rest] = [1, 2, 3]; // rest = [2, 3]
[p, q] = [q, p];                   // swap two variables
const { name, score } = player;    // objects: by property name
const { target } = event;          // same as event.target
for (const [x, y] of points) { }   // destructure in a loop
```

**`for...of` vs `forEach`**

| | `for...of` | `forEach` |
|---|---|---|
| Stop early (`break`/`return`) | ✅ Yes | ❌ No: `return` only exits the callback |
| Skip an item | `continue` | `return` in the callback |
| Get the index | `for (const [i, x] of arr.entries())` | `arr.forEach((x, i) => ...)` |
| Works on | Any iterable (arrays, strings, `NodeList`, `Map`, `Set`) | Arrays (and `NodeList`) |
| `await` inside | ✅ Waits for each | ❌ Doesn't wait |

- Use `forEach` to do something to every item (e.g. adding click handlers).
- Use `for...of` when you might stop early or are searching (e.g.
  `checkWinner`).
- Avoid `for...in` on arrays: it gives the **keys** (indices as strings),
  not the values.

**Order of checks matters.** Check for a win *before* a draw: if the last move
fills the board and completes a line, it's a win.

**`array.includes(value)`** returns `true` if the value is in the array.
`!board.includes("")` means "no empty squares left".

**Backticks only when needed.** Use template literals when there's a `${}` in
the string; otherwise ordinary quotes are fine.

**Format your code** in VS Code with **Shift+Alt+F**.

## Step 5: Restart button (in progress)

Task:

1. Get the `#restart` button and add a click handler to it.
2. In the handler, reset all the game state: `board`, `currentPlayer` and
   `gameOver`.
3. Clear the text from every cell on screen.
4. Reset the status message.
5. Tidy up: put the reset code in a function `resetGame()`, and think about
   whether the status-message code is repeated anywhere and could be a small
   function too.

Check: play a game to a win, click Restart, and you can play a fresh game
starting with X. Do the same after a draw, and mid-game.

---

## Learning roadmap (beyond this project)

1. **Basics:** `let`/`const`, types, functions, arrow functions, arrays and
   objects (`map`, `filter`, `forEach`), control flow, the DOM
   (`querySelector`, `addEventListener`), and using DevTools.
   Resources: [MDN JavaScript Guide](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide),
   [javascript.info](https://javascript.info).
2. **Small DOM games:** rock-paper-scissors, then noughts and crosses (this
   project), then a memory card game.
3. **Canvas and the game loop:** `<canvas>` 2D API, `requestAnimationFrame`,
   delta time, input, AABB collision, sprites. Build Pong, then Breakout, then a
   simple platformer.
4. **"Proper" web programming:** ES modules, classes, Promises,
   `async`/`await`, `fetch`, `localStorage`, Git, a local dev server.
5. **Libraries:** Phaser (2D), three.js (3D).

### Tips

- Read the module brief and marking criteria first.
- Commit to Git often with clear messages.
- Write the code yourself. Use AI to explain errors and concepts, not to write
  assessed work. Check your university's rules.
