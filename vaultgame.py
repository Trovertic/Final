from tkinter import *
from tkinter import ttk
import random

class VaultGame:
    MAX_HISTORY = 5
    STARTING_LIFES = 5

    def __init__(self):
        self.root = Toplevel()
        self.root.title("Vault Cracker")
        self.mainframe = ttk.Frame(self.root)
        self.mainframe.grid(column=0, row=0)

        self.lifes = self.STARTING_LIFES
        self.lifes_container = StringVar()
        self.lifes_container.set(f"Lives: {self.lifes}")
        self.size = 4

        self.label_sets = []

        self.code = []

        self.guess_inputs = []
        self.guess = []

        self.guess_count = 0
        self.guess_container = StringVar()
        self.guess_container.set(f"Total attempts: {self.guess_count}")
        

        self.create_instructions()
        # Create secret code
        self.create_code()
        # Create inputes
        self.create_inputs()
        # Fill labels
        self.init_labels()

        # Label to display attempts
        self.guess_label = ttk.Label(self.mainframe, textvariable=self.guess_container)
        self.guess_label.grid(column=self.size + 1, row=1)

        self.lifes_label = ttk.Label(self.mainframe, textvariable=self.lifes_container)
        self.lifes_label.grid(column=self.size + 1, row=0)

        # Button to submit guess's
        self.submit = ttk.Button(self.mainframe, text="Submit")
        self.submit["command"] = self.submit_guess
        self.submit.grid(column=self.size + 1, row=self.MAX_HISTORY + 1)


    # Create a window to show game instructions
    def create_instructions(self):
        new = Toplevel()
        self.info = ttk.Frame(new)
        self.info.grid(column=0, row=0)
        wrong = ttk.Label(self.info, font="15", text="Red means the number does not exist", background="#FF6767")
        kinda = ttk.Label(self.info, font="15", text="Yellow means the number exists but is in the wrong spot", background="#FFFC4F")
        kinda2 = ttk.Label(self.info, font="15", text="Blue means there are multiple of this number but is in the wrong spots", background="#6F9DFF")
        yes = ttk.Label(self.info, font="15", text="Green means the number is correct", background="#94FF94")

        wrong.grid(column=0, row=0)
        kinda.grid(column=0, row=1)
        kinda2.grid(column=0, row=2)
        yes.grid(column=0, row=3)

    # Fill all attempt slots with default values
    def init_labels(self):
        placeholder = "-" * self.size
        for _ in range(self.MAX_HISTORY):
            label_set = []
            for idx, letter in enumerate(placeholder):
                slot = ttk.Label(self.mainframe, anchor="center", width=2, font=20, text=letter, relief="groove", background=self.check_guess(idx, letter), borderwidth=1, padding="10 10 10 10")
                slot.grid(column=idx, row=len(self.label_sets))
                label_set.append(slot)
            self.label_sets.append(label_set)


    # Create dropdown boxes for each possible number
    def create_inputs(self):
        self.guess_inputs = []
        for i in range(self.size):
            self.guess_inputs.append(ttk.Combobox(self.mainframe, width=3))
            self.guess_inputs[i].grid(column=i, row=self.MAX_HISTORY + 1)
            self.guess_inputs[i]["values"] = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)


    # Creates random vault code
    def create_code(self):
        self.code = [random.randint(0, 9) for _ in range(self.size)]


    # Updates the current guess from the dropdown boxes
    def update_guess(self):
        guess = []
        for number in self.guess_inputs:
            if number.get().isdigit():
                guess.append(int(number.get()))
            else:
                return
        self.guess = guess
        self.guess_count += 1
        self.update_guess_display()

    
    # Updates the guess display container
    def update_guess_display(self):
        self.guess_container.set(f"Total attempts: {self.guess_count}")


    # Updates the lifes display container
    def update_life_display(self):
        self.lifes_container.set(f"Lifes: {self.lifes}")


    # Submits the user's guess to be checked and added to history
    def submit_guess(self):
        self.update_guess()
        label_set = []

        if len(self.guess) != self.size:
               return

        for idx, number in enumerate(self.guess):
            slot = ttk.Label(self.mainframe, anchor="center", width=2, font=20, text=number, relief="groove", background=self.check_guess(idx, number), borderwidth=1, padding="10 10 10 10")
            slot.grid(column=idx, row=len(self.label_sets))
            label_set.append(slot)

        self.label_sets.append(label_set)

    # If more than 5 sets, remove the oldest
        if len(self.label_sets) > self.MAX_HISTORY:
            oldest_set = self.label_sets.pop(0)
            for label in oldest_set:
                label.destroy()

            # Re-grid the remaining labels
            for row_idx, label_set in enumerate(self.label_sets):
                for col_idx, label in enumerate(label_set):
                    label.grid(column=col_idx, row=row_idx)

        self.check_win()

    # Check the guessed number and color based on correctness
    def check_guess(self, index, number):
        color = ""
        if number == "-":
            color = ""
        elif self.code[index] == number:
            color = "#94FF94"
        elif self.code.count(number) == 1:
            color = "#FFFC4F"
            if self.code[self.code.index(number)] == self.guess[self.code.index(number)]:
                color = "#FF6767"
        elif self.code.count(number) > 1:
            color = "#6F9DFF"
        else:
            color = "#FF6767"

        return color

    # Check if you have guessed the correct code and open a new window if lost
    def check_win(self):
        if self.lifes > 0:
            if self.code == self.guess:
                temp = []
                winner = ttk.Label(self.mainframe, text="You win!!")
                winner.grid(column=self.size + 1, row=2)
                temp.append(winner)
                self.submit.config(state=DISABLED)

                next_vault = ttk.Button(self.mainframe, text="Next Vault")
                next_vault.grid(column=self.size + 1, row=3)
                temp.append(next_vault)
                next_vault["command"] = lambda temp=temp : self.next_vault(temp)
            else:
                self.lifes -= 1
                if self.lifes > 0:
                    self.update_life_display()
                else:
                    self.check_win()
        else:
            lose = Toplevel()
            lose.title(":(")
            frame = ttk.Frame(lose, padding="10 10 10 10")
            frame.grid(column=0, row=0)
            ttk.Label(frame, font="30", text=f"You lost.. The code was {self.code}").grid(column=0, row=0)
            ttk.Label(frame, font="30", text=f"Your last guess was: {self.guess}").grid(column=0, row=1)
            self.root.destroy()

    # Reset and create a new vault with incresed difficutly 
    def next_vault(self, items):
        self.destroy(items)
        self.lifes += 3
        self.size += 1
        self.update_guess_display()
        self.update_life_display()
        self.create_code()
        self.create_inputs()
        self.submit.grid(column=self.size + 1, row=self.MAX_HISTORY + 1)
        self.guess_label.grid(column=self.size + 1, row=0)
        self.lifes_label.grid(column=self.size + 1, row=1)
        for row in self.label_sets:
            for label in row:
                label.destroy()
        self.label_sets = []
        self.init_labels()
        self.submit.config(state=NORMAL)

    # Removes leftover elements
    def destroy(self, items):
        for item in items:
            item.destroy()