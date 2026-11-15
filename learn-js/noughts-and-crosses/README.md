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
- [ ] Step 4: Check for a win or a draw
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

## Step 4: Check for a win or a draw (in progress)

Task:

1. List every winning line as an array of indices. There are 8:
   3 rows, 3 columns and 2 diagonals, e.g.
   `const winningLines = [[0, 1, 2], [3, 4, 5], ... ];`
2. Write a function `checkWinner()` that loops over `winningLines`. For each
   line `[a, b, c]`, if `board[a]` is not empty and
   `board[a] === board[b] && board[a] === board[c]`, return `board[a]`.
   Otherwise return `null` after the loop.
   Hint: destructuring, `const [a, b, c] = line;`
3. After each move (before switching player), call `checkWinner()`. If there
   is a winner, show `` `Player ${winner} wins!` `` and stop the game.
4. A draw is when there's no winner and every square is filled. Look up
   `board.includes("")` or `board.every(...)`.
5. Add `let gameOver = false;` and ignore clicks when it is `true`.

Check: X wins across the top row, O wins on a diagonal, a full board with no
line says it's a draw, and no clicks work after the game ends.

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
