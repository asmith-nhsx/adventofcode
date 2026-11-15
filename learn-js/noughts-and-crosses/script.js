// Step 1: check the script is connected.
// Open DevTools (F12) -> Console tab to see this message.
console.log("script.js is loaded!");

let board = ["", "", "", "", "", "", "", "", ""];
let currentPlayer = "X";

const cells = document.querySelectorAll(".cell");
const statusMsg = document.getElementById("status");

cells.forEach((cell) => {
  cell.addEventListener("click", (event) => {
    console.log(`Cell clicked ${event.target.dataset.index}`);
    let index = parseInt(event.target.dataset.index);
    if (board[index] === "") {
      board[index] = currentPlayer;
      event.target.textContent = currentPlayer;
      currentPlayer = currentPlayer === "X" ? "O" : "X";
      statusMsg.textContent = `Current player: ${currentPlayer}`;
    }
  });
});
