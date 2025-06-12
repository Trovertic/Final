import sudokugame, vaultgame, lightsgame, wordlegame, minesweeper
from tkinter import *
from tkinter import ttk

# Functions for creating windows
def create_sudoku_solver():
    sudokugame.SudokuSolver()

def create_vault_game():
    vaultgame.VaultGame()

def create_lights_game():
    lightsgame.LightsGame()

def create_wordle_game():
    wordlegame.Wordle()

def create_mines_game():
    minesweeper.Minesweeper()

# Setup tkinter
root = Tk()
root.title("Puzzle Pal")
root.geometry("280x140")
mainframe = ttk.Frame(root, padding="90 5 5 5")
mainframe.grid(column=0, row=0, sticky=("N, E, S, W"))

# Suduko solver
soduko = ttk.Button(mainframe, text="Sudoku solver")
soduko["command"] = create_sudoku_solver
soduko.grid(column=0, row=0, sticky=("N, E, S, W"))

# Vault cracking game
vault = ttk.Button(mainframe, text="Vault Cracker")
vault["command"] = create_vault_game
vault.grid(column=0, row=1)

# Wordle game
word = ttk.Button(mainframe, text="Wordle")
word["command"] = create_wordle_game
word.grid(column=0, row=2)

# Lights on puzzle
lights = ttk.Button(mainframe, text="Lights Puzzle")
lights["command"] = create_lights_game
lights.grid(column=0, row=3)

mines = ttk.Button(mainframe, text="Minesweeper")
mines["command"] = create_mines_game
mines.grid(column=0, row=4)


root.mainloop()
