# Sudoku-Solver
An algorithm that solves sudoku boards.

## How does it work
This algorithm solves sudoku boards that are represented as a 9x9 NumPy array. Empty cells are represented with the number '0' and if the board is unsolvable, the algorithm would return a board filled with '-1's. This algorithm uses the forward checking algorithm to check if the numbers, starting from 1 to 9, can be inserted into a cell in a valid manner. The algorithm continues to add numbers into the remaning cells until no numbers can be inserted due to invalidity. The algorithm then backtracks and restores its state before the previous number was added. This happens recursively until a solution is found, or if no solution is found.

## Demo Video
Results of the algorithm with 45 different boards from 4 difficulties.

![Demo](./gif/results_gif.gif)
