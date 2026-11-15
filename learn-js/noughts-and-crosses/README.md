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
- [ ] Step 2: Make clicks do something
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

## Step 2: Make clicks do something (in progress)

Task: write this yourself in `script.js`:

1. Use `document.querySelectorAll(".cell")` to get all 9 squares and store them
   in a `const`.
2. Loop over them with `.forEach(...)`.
3. Give each one a click handler with `addEventListener("click", ...)`.
4. In the handler, `console.log` the clicked square's index.
   Hint: `event.target.dataset.index`.

If it works, clicking squares prints `0`, `4`, `8` and so on in the console.

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
