from tkinter import *
from tkinter import ttk
from random import randint

class Minesweeper:
    SIZE = 10
    MAX_BOMBS = 10
    CLICKED_COLOR = "#999999"
    SAFE_COLOR = "#D1D1D1"
    BOMB_COLOR = "#FF0000"
    FLAG_COLOR = "#FFF132"
    BOMB = "✕"
    FLAG = "Δ"
    SAFE = 0
    
    def __init__(self):
        root = Toplevel()
        root.title("Minesweeper")
        self.mainframe = ttk.Frame(root, padding="10 10 10 10")
        self.mainframe.grid(column=0, row=0)

        self.gameframe = ttk.Frame(self.mainframe, padding="10 10 10 10")
        self.gameframe.grid(column=0, row=0)

        self.buttonframe = ttk.Frame(root, padding="10 10 10 10")
        self.buttonframe.grid(column=0, row=2)

        self.info_text = StringVar()
        self.info = ttk.Label(self.mainframe, textvariable=self.info_text)
        self.info.grid(column=0, row=1)

        self.clicking_var = BooleanVar()
        self.clicking = ttk.Checkbutton(self.buttonframe, text="Click!", variable=self.clicking_var)
        self.clicking.grid(column=0, row=0)

        self.flag_var = BooleanVar()
        self.flag = ttk.Checkbutton(self.buttonframe, text="Flag", variable=self.flag_var)
        self.flag.grid(column=2, row=0)

        self.newgame_button = ttk.Button(self.buttonframe, command=self.newgame , text="New Game")
        self.newgame_button.grid(column=1, row=3)

        self.grid = []
        self.gridvalues = []
        self.gridprediction = []

        self.flag_count = 0

        self.newgame()

    def create_grid(self):
        for y in range(self.SIZE):
            grid_row = []
            for x in range(self.SIZE):
                grid_row.append(Button(self.gameframe, width=3, padx=1, pady=1, background=self.SAFE_COLOR))
                grid_row[x].grid(column=x, row=y)
                grid_row[x]["command"] =lambda grid_info=grid_row[x].grid_info() : self.box_clicked(grid_info)
            self.grid.append(grid_row)

        self.gridvalues = [[0 for _ in range(self.SIZE)] for _ in range(self.SIZE)]
        self.gridprediction = [[0 for _ in range(self.SIZE)] for _ in range(self.SIZE)]
    
    
    def box_clicked(self, grid_info, visited=None):
        x = grid_info["column"]
        y = grid_info["row"]

        if self.clicking_var.get() == True and self.flag_var.get() == False:
            if visited is None:
                visited = set()
            if (y, x) in visited:
                return
            visited.add((y, x))
            if self.gridprediction[y][x] <= 1:  # Allow clicking for 0 or 1
                self.toggle(y, x)
                self.check_connected(y, x, visited)
            elif self.gridprediction[y][x] == 10:
                self.toggle(y, x)
                print("Lose")
            else:
                self.toggle(y, x)

        elif self.flag_var.get() == True and self.clicking_var.get() == False:
            if self.grid[y][x]["background"] == self.FLAG_COLOR:
                self.grid[y][x]["background"] = self.SAFE_COLOR
                self.grid[y][x]["text"] = ""
                self.flag_count -= 1
            else:
                if self.flag_count < self.MAX_BOMBS:
                    self.grid[y][x]["background"] = self.FLAG_COLOR
                    self.grid[y][x]["text"] = self.FLAG
                    self.flag_count += 1
        else:
            pass

        self.check_win()


    def toggle(self, y, x):
        if self.gridvalues[y][x] == self.SAFE:
            self.grid[y][x].config(state=DISABLED, background=self.CLICKED_COLOR, text=self.gridprediction[y][x])
        elif self.gridvalues[y][x] == self.BOMB:
            self.grid[y][x].config(state=DISABLED, background=self.BOMB_COLOR, text=self.gridprediction[y][x])

    
    def check_connected(self, y, x, visited):
        if self.gridprediction[y][x] > 1:
            return
        directions = [(-1,0), (1,0), (0,-1), (0,1)]
        for dy, dx in directions:
            ny, nx = y + dy, x + dx
            if 0 <= ny < self.SIZE and 0 <= nx < self.SIZE:
                if self.check_valid(ny, nx) and (ny, nx) not in visited:
                    self.box_clicked(self.grid[ny][nx].grid_info(), visited)


    def check_valid(self, y, x):
        try:
            if (
                self.grid[y][x] is not None
                and self.grid[y][x]["background"] != self.CLICKED_COLOR
                and self.gridprediction[y][x] <= 1  # Allow both 0 and 1
            ):
                return True
            else:
                return False
        except IndexError:
            return False
        
    
    def set_bombs(self):
        for _ in range(self.MAX_BOMBS):
            rany = randint(0, self.SIZE - 1)
            ranx = randint(0, self.SIZE - 1)
            if self.gridvalues[rany][ranx] == 0:
                self.gridvalues[rany][ranx] = self.BOMB
        self.info_text.set("Find all the bombs")

    
    def update_prediction(self):
        for y in range(self.SIZE):
            for x in range(self.SIZE):
                if self.gridvalues[y][x] == self.BOMB:
                    self.gridprediction[y][x] = 10
                    continue
                count = 0
                for iy in range(-1, 2):
                    for ix in range(-1, 2):
                        ny = y + iy
                        nx = x + ix
                        if 0 <= ny < self.SIZE and 0 <= nx < self.SIZE:
                            if self.gridvalues[ny][nx] == self.BOMB:
                                count += 1
                self.gridprediction[y][x] = count

        
    def check_win(self):
        count = 0
        for y in range(self.SIZE):
            for x in range(self.SIZE):
                if self.gridvalues[y][x] == self.BOMB and self.grid[y][x]["background"] == self.FLAG_COLOR:
                    count += 1
        if count == self.MAX_BOMBS:
            self.info_text.set("You win!")


    
    def newgame(self):
        if len(self.grid) > 0:
            for row in self.grid:
                for button in row:
                    button.destroy()
        self.grid = []
        self.create_grid()
        self.set_bombs()
        self.update_prediction()
