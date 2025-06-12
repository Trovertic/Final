from tkinter import *
from tkinter import ttk
from random import randint

class LightsGame:
    ON = "#FFFCD2"
    OFF = "#5F5F5F"

    def __init__(self):

        self.root = Toplevel()
        self.root.title("Lights Game")
        self.mainframe = ttk.Frame(self.root)
        self.mainframe.grid(column=0, row=0)
        self.buttons = []
        self.size = 5
        self.difficutly = 4
        self.next_button = None
        self.attempts_container = StringVar()
        self.attempts = 0
        self.attempts_label = ttk.Label(self.mainframe, textvariable=self.attempts_container)
        self.text_container = StringVar()
        self.text_label = ttk.Label(self.mainframe, textvariable=self.text_container)

        ttk.Label(self.mainframe, text="Turn off all the lights to win!", padding="10 10 10 10").grid(column=self.size + 2, row=0)

        self.new_game()


    # Place all the buttons in the widget
    def create_buttons(self):

        # Check for existing buttons
        if len(self.buttons) > 0:
            for row in self.buttons:
                for button in row:
                    button.destroy()
        if self.next_button != None:
            self.next_button.destroy()
        
        self.next_button = Button(self.mainframe, text="New")
        self.next_button.grid(column=self.size + 1, row=0)
        self.next_button["command"] = self.new_game

        # self.solve_button = Button(self.mainframe, text="Solve")
        # self.solve_button.grid(column=self.size + 1, row=1)
        # self.solve_button["command"] = self.solve_puzzle


        # Fill the buttons with a default symbol
        self.buttons = [[Button(self.mainframe, text="●", width=3, background=self.ON, padx=10, pady=10) for _ in range(self.size)] for _ in range(self.size)]
 
        for i in range(self.size):
            for j in range(self.size):
                self.buttons[i][j].grid(column=j, row=i)
                self.buttons[i][j]["command"] = lambda button=self.buttons[i][j].grid_info() : self.button_clicked(button)


    # Check if a button exists
    def is_valid(self, y, x):
        if x >= 0 and x <= self.size - 1 and y >= 0 and y <= self.size - 1:
            return True
        else:
            return False
        
    
    # def is_off(self, y, x):
    #     if self.buttons[y][x]["background"] == self.OFF:
    #         return True
    #     else:
    #         return False
        
    
    # Update attempts label
    def update_attempts(self):
        self.attempts_container.set(f"Attempts: {self.attempts}")
        self.attempts_label.grid(column=self.size + 1, row=self.size - 1)

    # Update info label
    def update_text(self):
        self.text_container.set("")
        self.text_label.grid(column=self.size + 1, row=self.size - 2)

    # When clicked toggle surounding lights
    def button_clicked(self, grid_info):
        self.attempts += 1
        self.update_attempts()

        x = grid_info["column"]
        y = grid_info["row"]

        for i in range(3):
            if self.is_valid(x - 1 + i, y):
                self.toggle_light(self.buttons[y][x - 1 + i])
            if self.is_valid(x, y - 1 + i):
                self.toggle_light(self.buttons[y - 1 + i][x])
        self.toggle_light(self.buttons[y][x])

        self.check_win()

    # Turn on or off a light
    def toggle_light(self, button):
        if button["background"] == self.ON:
            button["background"] = self.OFF
        else:
            button["background"] = self.ON

    # Creates the game board
    def new_game(self):
        self.create_buttons()
        self.update_attempts()
        self.update_text()

        self.attempts = 0 - self.difficutly
        
        for _ in range(self.difficutly):
            button = self.buttons[randint(0, self.size - 1)][randint(0, self.size - 1)]
            self.button_clicked(button.grid_info())

    # Check if all lights are on
    def check_win(self):
        for row in self.buttons:
            for button in row:
                if button["background"] != self.OFF:
                    return False
        
        self.text_container.set("You Win!")


    # def solve_puzzle(self):
    #     for i in range(self.size):
    #         for j in range(self.size):
    #             if not self.is_valid(i - 1, j):
    #                 continue
    #             else:
    #                 if self.is_off(i - 1, j):
    #                     self.button_clicked(self.buttons[i][j].grid_info())
    #                 if i >= self.size and j >= self.size:
    #                     return False





                    
