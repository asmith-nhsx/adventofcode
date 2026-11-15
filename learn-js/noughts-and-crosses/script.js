// Step 1: check the script is connected.
// Open DevTools (F12) -> Console tab to see this message.
console.log("script.js is loaded!");

let board = ["", "", "", "", "", "", "", "", ""];
let currentPlayer = "X";

const cells = document.querySelectorAll(".cell");
const statusMsg = document.getElementById("status");
const winningLines = [
  [0, 1, 2],
  [3, 4, 5],
  [6, 7, 8],
  [0, 3, 6],
  [1, 4, 7],
  [2, 5, 8],
  [0, 4, 8],
  [2, 4, 6],
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

cells.forEach((cell) => {
  cell.addEventListener("click", (event) => {
    if (gameOver) return;
    const index = parseInt(event.target.dataset.index);
    console.log(`Cell clicked ${index}`);
    if (board[index] === "") {
      board[index] = currentPlayer;
      event.target.textContent = currentPlayer;
      const winner = checkWinner();
      if (winner !== null) {
        gameOver = true;
        statusMsg.textContent = `Player ${currentPlayer} wins!`;
        return;
      }
      if (!board.includes("")) {
        gameOver = true;
        statusMsg.textContent = "It's a draw!";
        return;
      }
      currentPlayer = currentPlayer === "X" ? "O" : "X";
      statusMsg.textContent = `Player: ${currentPlayer}'s turn`;
    }
  });
});
