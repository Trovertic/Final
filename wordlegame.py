from tkinter import *
from tkinter import ttk
from random import randint

class Wordle:
    MAX_HISTORY = 5

    def __init__(self):
        root = Toplevel()
        root.title("Wordle")
        self.mainframe = ttk.Frame(root, padding="10 10 10 10")
        self.mainframe.grid(column=0, row=0)

        # Get list of words from file
        self.words = []
        with open("words") as w:
            for _ in range(3103):
                self.words.append(w.readline().strip())
        
        self.label_sets = []
        self.word = ""
        self.get_random_word()

        self.guess = ""
        self.attempts = 0

        self.guess_input = ttk.Entry(self.mainframe)
        self.submit = ttk.Button(self.mainframe, text="Submit")
        self.submit["command"] = self.submit_guess

        self.info_container = StringVar()
        self.info_label = ttk.Label(self.mainframe, textvariable=self.info_container)

        self.new_word = ttk.Button(self.mainframe, text="New Word")
        self.new_word["command"] = self.new_game

        self.create_instructions()

        self.new_game()

    # Creates a new game
    def new_game(self):
        self.attempts = 0
        self.get_random_word()
        self.init_labels()
        self.update_elements()
        self.submit.config(state=NORMAL)

    # Updates placment and display of elements
    def update_elements(self):
        self.info_label.grid(column=6, row=1)
        self.guess_input.grid(column=6, row=4)
        self.new_word.grid(column=6, row=2)
        self.submit.grid(column=6, row=3)

    # Picks a random word
    def get_random_word(self):
        self.word = self.words[randint(0, len(self.words) - 1)]
    
    # Stores users guess and clears entry box
    def update_guess(self):
        self.guess = self.guess_input.get().lower()
        self.guess_input.destroy()
        self.guess_input = ttk.Entry(self.mainframe)
        self.guess_input.grid(column=6, row=4)

    # Create initial labels
    def init_labels(self):
        placeholder = "-----"
        if len(self.label_sets) > 0:
            for row in self.label_sets:
                for label in row:
                    label.destroy()
            self.label_sets = []

        for _ in range(5):
            label_set = []
            for idx, letter in enumerate(placeholder):
                slot = ttk.Label(self.mainframe,anchor="center", font="20", width=2, text=letter, relief="groove", background=self.check_guess(idx, letter), borderwidth=1, padding="10 10 10 10")
                slot.grid(column=idx, row=len(self.label_sets))
                label_set.append(slot)
            self.label_sets.append(label_set)

    # Create a window for instructions
    def create_instructions(self):
        new = Toplevel()
        self.info = ttk.Frame(new)
        self.info.grid(column=0, row=0)
        wrong = ttk.Label(self.info, font="15", text="Red means the letter does not exist", background="#FF6767")
        kinda = ttk.Label(self.info, font="15", text="Yellow means the letter exists but is in the wrong spot", background="#FFFC4F")
        kinda2 = ttk.Label(self.info, font="15", text="Blue means there are multiple of this letter but is in the wrong spots", background="#6F9DFF")
        yes = ttk.Label(self.info, font="15", text="Green means the letter is correct", background="#94FF94")

        wrong.grid(column=0, row=0)
        kinda.grid(column=0, row=1)
        kinda2.grid(column=0, row=2)
        yes.grid(column=0, row=3)

    # Stores users guess and prints the labels according to correctness
    def submit_guess(self):
        self.update_guess()
        if not self.check_valid_word():
            self.info_container.set("Must be a valid word")
            return
        self.info_container.set("")

        label_set = []

        if len(self.guess) != 5:
               return

        # Creats a label for every letter in word
        for idx, letter in enumerate(self.guess):
            slot = ttk.Label(self.mainframe,anchor="center", font="20", width=2, text=letter, relief="groove", background=self.check_guess(idx, letter), borderwidth=1, padding="10 10 10 10")
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

        # Check if user can still win
        if self.attempts < 5:
            if self.check_win():
                self.info_container.set("You found the word! :)")
                self.submit.config(state=DISABLED)
            else:
                self.attempts += 1
        if self.attempts == 5:
            self.info_container.set(f"You failed to solve '{self.word}'")
            self.submit.config(state=DISABLED)

    # Checks how close the users guess is to the chosen word
    def check_guess(self, index, letter):
        color = ""
        if letter == "-":
            return
        elif self.word[index] == letter:
            color = "#94FF94"
        elif self.word.count(letter) == 1:
            color = "#FFFC4F"
            if self.word[self.word.index(letter)] == self.guess[self.word.index(letter)]:
                color = "#FF6767"
        elif self.word.count(letter) > 1:
            color = "#6F9DFF"
        else:
            color = "#FF6767"

        return color
        
    # Checks if the users guess exists in the word list
    def check_valid_word(self):
        if self.words.count(self.guess) > 0:
            return True
        else:
            return False
        
   # Check if user has guessed the word 
    def check_win(self):
        if self.word == self.guess:
            return True
        else:
            return False