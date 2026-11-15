// Step 1: check the script is connected.
// Open DevTools (F12) -> Console tab to see this message.
console.log("script.js is loaded!");
const cells = document.querySelectorAll(".cell");
cells.forEach((cell) => {
  cell.addEventListener("click", (event) => {
    console.log(`Cell clicked ${event.target.dataset.index}`);
  });
});