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
- [ ] Step 3: Store the board in an array and take turns between X and O
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

## Step 3: Store the board and take turns (in progress)

Task:

1. Create the "real" board: `let board = ["", "", "", "", "", "", "", "", ""];`
   (or `Array(9).fill("")`).
2. Create `let currentPlayer = "X";`
3. In the click handler, get the index as a number.
4. If `board[index]` is already filled, `return` early (ignore the click).
5. Otherwise set `board[index] = currentPlayer` and show it on screen with
   `cell.textContent = currentPlayer`.
6. Switch players: if it was `"X"`, make it `"O"`, and vice versa.
   Try writing it with `if/else` first, then with the ternary operator
   `condition ? a : b`.
7. Update the `#status` paragraph to show `` `Player ${currentPlayer}'s turn` ``.

Check: clicks alternate X/O, clicking a filled square does nothing, and
`console.log(board)` shows the array filling up.

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
