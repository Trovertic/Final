# Puzzle Pal
#### Video: <url>

 Hello, this is my final project for cs50. I was unsure about what I should do for said project. At first, I wanted to try and make a webapp but have learned that web dev is not my friend. But after some time pondering, I decided that I could learn a new UI instead and went with tkinter instead.

To help sharpen my programming skill I decided to make Puzzle Pal! A small showcase of recreated puzzle games to pass your time with. To me it sounded like a great way to work on my problem-solving skills while also learning more about UI.

### Main.py
This is the heart of the project and where tkinter’s mainloop is created. A simple interface to navigate the recreated games within. There wasn't much thought that when into this part of the project. I just wanted a place to keep everything tied together.

### Sudoku
Sudoku was the first part of this project I tried to tackle. I have read in many places online that making a sudoku solver was a great practice exercise and figured it would be a great fit. Here is where I spend most of my time really trying to learn how tkinter works. The first task on my mind was making a grid to hold all the numbers for the puzzle.
A 2d array (9x9 grid) was the perfect starting point in my mind and after learning how to create the initial frames for the UI, I started to populate the array with dropdown entries to select any number 1-9. To do this, I first created cells comprised of a 3x3 grid of numbers. I do this 9 times and combine them to create the full 9x9 grid. Then I needed to find a way to extract the number data from each cell and reorganize it to fit the full 9x9 grid.
Now that I have my fully populated 9x9 grid of values it’s time to solve. I was unsure what approach I should go for. At first, I thought of making 3 separate lists, one for each check (Vertical, Horizontal, and the cell itself) After some time trying to implement this idea I ran into some issues and figured there must be a better way. So, I tried to break it down more simply and checked numbers one by one. First by getting the location to try to put each number in said spot then checking each location one by one related to the starting point to see if the number can be placed there. If it can, then place that number in that location and repeat this process. Once it has checked every location it goes back to double check as many times as needed to ensure that every location is still valid. Then I simply created a new window showing the result. Easy as that!

### Vault Cracker
This was the second task I started to work on. I wanted to make something similar to the game Wordle but simpler and with numbers instead of words. After spending much time in Sudoku figuring out how to use tkinter this was a much easier task to create the interface. This game also uses dropdown boxes to select the numbers you would like to guess. The challenge in this project was creating the Interface to show guess history. Luckly for me my first idea for this problem was a working solution. I created a grid of empty labels to fill the board and stored them in an 2d array. After each guess you submit it would add a new row of labels to said array and delete the oldest set followed by updating the display accordingly. Each label is also checked for correctness and color coded accordingly. After each solved vault, the length of the code increases until you run out of lives.

### Wordle
After finishing Vault Cracker I figured I would go ahead and remake the original as well. It follows the same idea as vault cracker though I feel I was a bit more organized this time around in making it. It uses a list of 3000+ words provided from ChatGPT and picks randomly one for each game you start. The word you guess must be included in that list as well. This list could be bigger but for most cases this list is large enough.

### Lights Puzzle
Lights out is a puzzle where you have a grid of buttons typically 3x3 – 5x5 where some buttons are lite up and others are dark. The goal is to turn off every light in the puzzle. The trick is when you toggle a light, it will also turn on or off surrounding lights in a cross pattern if possible. To do this I first created a 5x5 grid of buttons and created separate functions for toggling the light as well as clicking the button to check the surrounding area. If a button is found around the clicked button, then it will toggle said light, easy as that. Once all the lights are off you win!
