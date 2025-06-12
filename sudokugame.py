from tkinter import *
from tkinter import ttk

class SudokuSolver:
    def __init__(self):
        # Create app
        root = Toplevel()
        root.title("Sudoku Solver")

        # Setup mainframe
        self.mainframe = ttk.Frame(root, padding="10 10 10 10")
        self.mainframe.grid(column=0, row=0)

        # Create the the game grid
        self.grid_entry = [[IntVar() for _ in range(9)] for _ in range(9)]

        # Default grid for testing and showcase
        puzzle = [[8, 3, 0, 4, 0, 5, 0, 2, 0],
                [9, 0, 0, 7, 0, 0, 0, 5, 8],
                [1, 5, 6, 0, 2, 0, 3, 0, 0],
                [0, 0, 8, 0, 7, 2, 5, 0, 0],
                [7, 0, 5, 0, 3, 0, 6, 0, 0],
                [0, 6, 0, 0, 4, 9, 8, 0, 2],
                [2, 0, 0, 0, 0, 0, 4, 6, 9],
                [0, 0, 0, 0, 8, 4, 7, 0, 0],
                [5, 0, 4, 0, 0, 0, 0, 8, 1]]

        self.grid = puzzle #[[0 for _ in range(9)] for _ in range(9)]

        # Update all cell entries to grid values
        for i in range(9):
            for k in range(9):
                self.grid_entry[i][k].set(self.grid[i][k])
                
        # Create all input cell blocks
        self.cells = []
        for block_row in range(3):
            for block_col in range(3):
                block_vars = []
                for i in range(3):
                    for j in range(3):
                        row = block_row * 3 + i
                        col = block_col * 3 + j
                        block_vars.append(self.grid_entry[row][col])
                self.cells.append(InputCell(self.mainframe, block_vars, block_col, block_row))

        # Create buttons for solve and reset
        solve = ttk.Button(self.mainframe, text="Solve")
        solve.grid(column=0, row=3)
        solve["command"] = self.update_grid

        reset = ttk.Button(self.mainframe, text="Reset")
        reset.grid(column=2, row=3)
        reset["command"] = self.reset

        self.info = StringVar()
        self.info.set("Waiting for puzzle..")
        ttk.Label(self.mainframe, textvariable=self.info).grid(column=3, row=1)


    # Update grid values
    def update_grid(self):
        # Create an empty 9x9 grid
        new_grid = [[0 for _ in range(9)] for _ in range(9)]

        # Each cell is a 3x3 block, and there are 9 cells arranged in a 3x3 grid
        for cell_index, cell in enumerate(self.cells):
            cell_values = cell.get_values()
            # Convert all values to int, treat empty as 0
            for index, number in enumerate(cell_values):
                if str(number).isdigit():
                    cell_values[index] = int(number)
                else:
                    cell_values[index] = 0

            # Find the new grids position in the 3x3 grid of blocks
            new_grid_row = cell_index // 3
            new_grid_col = cell_index % 3

            # Place each value in the correct spot in the 9x9 grid
            for i in range(3):
                for j in range(3):
                    row_index = new_grid_row * 3 + i
                    col_index = new_grid_col * 3 + j
                    new_grid[row_index][col_index] = cell_values[i * 3 + j]

        self.grid = new_grid


        if not self.is_initial_grid_valid():
            self.info.set("Invalid puzzle")
        elif self.solve():
            self.info.set("Solution found! :)")
            self.display_solution()
        else:
            self.info.set("No solution :(")


    # Check if a number is valid at x y
    def check_valid(self, y, x, n):
        for i in range(9):
            if int(self.grid[y][i]) == n:
                return False
            
        for i in range(9):
            if int(self.grid[i][x]) == n:
                return False
            
        y0 = (y//3)*3
        x0 = (x//3)*3
        for i in range(3):
            for j in range(3):
                if int(self.grid[y0 + i][x0 + j]) == n:
                    return False
        return True


    # Check if the puzzle is valid to prevent infinite loops
    def is_initial_grid_valid(self):
        for y in range(9):
            for x in range(9):
                n = self.grid[y][x]
                if n != 0:
                    # Temporarily remove the number to check for duplicates
                    self.grid[y][x] = 0
                    if not self.check_valid(y, x, n):
                        self.grid[y][x] = n
                        return False
                    self.grid[y][x] = n
        return True


    # Check for valid options and apply them to the grid
    def solve(self):
        for y in range(9):
            for x in range(9):
                if int(self.grid[y][x]) == 0:
                    for n in range(1, 10):
                        if self.check_valid(y, x, n):
                            self.grid[y][x] = n
                            if self.solve():
                                return True
                            self.grid[y][x] = 0  # Backtrack
                    return False  # No valid number found, trigger backtracking
        return True  # Solved
    
    # Resets all cells to 0
    def reset(self):
        self.info.set("Waiting for puzzle..")
        for cell in self.cells:
            cell.reset()


    # Create a new window to that displays the solution
    def display_solution(self):
        # Create app
        new_root = Toplevel()
        new_root.title("Solution")

        # Setup mainframe
        new_mainframe = ttk.Frame(new_root, padding="10 10 10 10")
        new_mainframe.grid(column=0, row=0)

        self.grid
        
        # Create all display cell blocks
        cells = []
        for block_row in range(3):
            for block_col in range(3):
                block_vars = []
                for i in range(3):
                    for j in range(3):
                        row = block_row * 3 + i
                        col = block_col * 3 + j
                        block_vars.append(self.grid[row][col])
                cells.append(DisplayCell(new_mainframe, block_vars, block_col, block_row))


class InputCell:
    def __init__(self, frame, grid, col, row):
        # Setup cell frame
        self.cell_frame = ttk.Frame(frame, relief="solid", borderwidth=5, padding="3 3 3 3")
        self.cell_frame.grid(column=col, row=row)

        self.grid = grid
        self.boxes = []

        x = 0
        y = 0
        # Create dropdown boxes for the cell
        for i in range(len(self.grid)):
            box = ttk.Combobox(self.cell_frame, width=1, textvariable=self.grid[i])
            box["values"] = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
            box.grid(column=x, row=y)
            box.set(self.grid[i].get())
            self.boxes.append(box)
            if x < 2:
                x += 1
            else:
                y += 2
                x = 0

    # Retunrs value from the combobox
    def get_values(self):
        grid = []
        for box in self.boxes:
            grid.append(box.get())
        return grid
    
    def reset(self):
        for box in self.boxes:
            box.set(0)
    

class DisplayCell:
    def __init__(self, frame, grid, col, row):
        # Setup cell frame
        self.cell_frame = ttk.Frame(frame, relief="solid", borderwidth=5, padding="3 3 3 3")
        self.cell_frame.grid(column=col, row=row)

        self.grid = grid
        self.boxes = []

        x = 0
        y = 0
        # Create dropdown boxes for the cell
        for i in range(len(grid)):
            box = ttk.Label(self.cell_frame, font="20", text=self.grid[i], padding="10 5 10 5")
            box.grid(column=x, row=y)
            self.boxes.append(box)
            if x < 2:
                x += 1
            else:
                y += 2
                x = 0
    