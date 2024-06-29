import time
import numpy as np
from solver import sudoku_solver

__SCORES = {}
# Load sudokus
sudoku = np.load("data/very_easy_puzzle.npy")
total_score = {}

difficulties = ['very_easy', 'easy', 'medium', 'hard']

for difficulty in difficulties:
    print(f"Testing {difficulty} sudokus")
    
    sudokus = np.load(f"data/{difficulty}_puzzle.npy")
    solutions = np.load(f"data/{difficulty}_solution.npy")
    
    count = 0
    for i in range(len(sudokus)):
        sudoku = sudokus[i].copy()
        print(f"This is {difficulty} sudoku number", i)
        print(sudoku)
        
        start_time = time.process_time()
        your_solution = sudoku_solver(sudoku)
        end_time = time.process_time()
        
        if not isinstance(your_solution, np.ndarray):
            print("\033[91m[ERROR] Your sudoku_solver function returned a variable that has the incorrect type. If you submit this it will likely fail the auto-marking procedure result in a mark of 0 as it is expecting the function to return a numpy array with a shape (9,9).\n\t\033[94mYour function returns a {} object when {} was expected.\n\x1b[m".format(type(your_solution), np.ndarray))
        elif not np.all(your_solution.shape == (9, 9)):
            print("\033[91m[ERROR] Your sudoku_solver function returned an array that has the incorrect shape.  If you submit this it will likely fail the auto-marking procedure result in a mark of 0 as it is expecting the function to return a numpy array with a shape (9,9).\n\t\033[94mYour function returns an array with shape {} when {} was expected.\n\x1b[m".format(your_solution.shape, (9, 9)))
        
        print(f"This is your solution for {difficulty} sudoku number", i)
        print(your_solution)
        
        print("Is your solution correct?")
        if np.array_equal(your_solution, solutions[i]):
            print("Yes! Correct solution.")
            count += 1
        else:
            print("No, the correct solution is:")
            print(solutions[i])
        
        print("This sudoku took {} seconds to solve.\n".format(end_time-start_time))

    total_score[f"{difficulty}"] = f"{count}/{len(sudokus)}"    
    print(f"{count}/{len(sudokus)} {difficulty} sudokus correct\n")

print("Overall Score:")
for difficulty in difficulties:
    print(f"{total_score[difficulty]} {difficulty} sudokus correct")
print()
__SCORES[difficulty] = {
    'correct': count,
    'total': len(sudokus)
}