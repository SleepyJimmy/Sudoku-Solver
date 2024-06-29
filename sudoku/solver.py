import numpy as np

def sudoku_solver(sudoku):
    """
    Solves a Sudoku puzzle and returns its unique solution.

    Input
        sudoku : 9x9 numpy array
            Empty cells are designated by 0.

    Output
        9x9 numpy array of integers
            It contains the solution, if there is one. If there is no solution, all array entries should be -1.
    """
    order_values = {}
    members = {}
    assigned_vars = {}
    sol_array = np.full((9, 9), None)
    
    # a tuple of variables represents the index of each cell in the sudoku board
    variables = [(i, j) for i in range(len(sudoku)) for j in range(len(sudoku))]
    
    # populate the values for every variable
    populate_order_values(sudoku, variables, order_values)

    # populate the members for every variable
    populate_members(sudoku, variables, members)
    
    # execute the backtracking algorithm
    solution = depth_first_search(sol_array, order_values, members, variables)
    
    
    if solution is None:
        return np.full((9, 9), -1)
    return solution
    

def populate_order_values(sudoku, variables, order_values):
    """
    This function populates the order_values dictionary. The keys are the cells (variables), while 
    the values are a set of possible values for that cell.
    
    If the cell is empty, AKA 0, then the values would be a range of numbers from 1-9 indicating 
    that those are all the possible numbers. 
    """    
    # for every variable, populate its possible values
    for var in variables:
        if sudoku[var[0]][var[1]] == 0:
            order_values[var] = set(range(1, 10))
        else:
            order_values[var] = {sudoku[var[0]][var[1]]}


def populate_members(sudoku, variables, members):
    """
    This function will add the cells in the same row, column, and 3x3 grid. 
    This is to check whether the same number already exists in these cells.
    
    The members dictionary will have the tuple variable as keys,
    and a list of tuples as the values, which represent the rows, columns, and 3x3 
    grid that the cell is a member of. 
    """
    # for every variable, populate its members
    for var in variables:
        # initialise members dict for a cell's value to be a list
        members[var] = []    
        row, col = var     
        
        # append all cells in the same row
        for j in range(len(sudoku[0])):
            if j != col:
                members[var].append((row, j))
                
        # append all cells in the same column
        for i in range(len(sudoku[0])):
            if i != row:
                members[var].append((i, col))
        
        # append all cells in the same 3x3 grid
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if var != (i, j):
                    members[var].append((i , j))

                    
def depth_first_search(sol_array, order_values, members, variables):
    """
    This is the backtracking algorithm. It performs a depth first search approach, 
    and when it hits a point where it cannot place any more new values into 
    any cells, it 'backtracks' and tries a different value from a cell that it
    has already visited. 
    """
    # Base case - if all cells in the array have been assigned a value
    if not None in sol_array:
        return sol_array
    
    # obtain an empty variable
    empty_var = get_empty_var(sol_array, order_values, variables)
    # if no more empty variables, but not solution
    if empty_var is None:
        return None 
    
    row, col = empty_var
    
    # for every value in its set of possible values
    for value in order_values[empty_var].copy():
        
        # if valid, assign that value to variable in array
        if is_valid(empty_var, value, members, sol_array):
            sol_array[row][col] = value
                    
            # create a backup dictionary
            old_order_values = {v: order_values[v].copy() for v in order_values}  
            
            # execute forward check, if valid, recursively call backtrack algorithm 
            if forward_check(empty_var, value, members, order_values):
                
                # recursively call the algorithm 
                solution = depth_first_search(sol_array, order_values, members, variables)
                
                # return solution if there is one
                if solution is not None:
                    return solution
                    
            # Restore possible values using backup dictionary if no solution found
            order_values.update(old_order_values)
            sol_array[row][col] = None
    return None


def get_empty_var(sol_array, order_values, variables):
    """
    Here, we are going to select an empty variable that has the smallest amount
    of values in its set of possible values.
    
    This uses the minimum remaining values heuristic by allowing the algorithm to 
    prioritise variables which are more likely to fail first. Thus, allowing
    the algorithm to know which variables can be ruled out earlier.
    """
    # append into a list all variables that have not been assigned
    empty_variables = []
    for var in variables:
        if sol_array[var[0]][var[1]] == None:
            empty_variables.append(var)
            
    # then choose the variable that has the least amount of possible values
    value_sizes = np.array([len(order_values[var]) for var in empty_variables])
    # argmin is used to find the index of the variable with the least amount of possible values
    return empty_variables[np.argmin(value_sizes)]


def is_valid(var, value, members, sol_array):
    """
    This function checks if inserting a number into a cell is valid
    with respect to the rules of sudoku.
    
    This uses the members dictionary and checks if the value 
    already exists in one of the members connected to that variable.
    """
    # if value already exists in any member variables, invalid
    for member_var in members[var]:
        if sol_array[member_var[0]][member_var[1]] == value:
            return False
    return True
                    
    
def forward_check(var, value, members, order_values):
    """
    The forward check function allows the algorithm to prune away the values of the variables
    that are included in the members of the current variable. It does this by removing the value
    from the possible values of cells. 
    
    Returns false if removing a value from the possible values of member cells, would cause 
    the amount of possible values to become 0. This would mean that the input value is invalid. 
    """
    # track the changes made in the algorithm
    changes = []
    
    # for every member variable, discard the value from their set of possible values 
    for member_var in members[var]:
        if value in order_values[member_var]:
            order_values[member_var].discard(value)
            changes.append(member_var)
            
            # invalid if discarding order_values causes a variable to have no more possible values
            if len(order_values[member_var]) == 0:
                # Restore values before returning False
                for changed_var in changes:
                    order_values[changed_var].add(value)
                return False
    return True
    