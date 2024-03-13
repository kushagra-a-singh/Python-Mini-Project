import tkinter as tk
from tkinter import messagebox
import random
import os
import sys
import json
import utils
from play_puzzle import play, draw_letters_honeycomb, ask_user, help as play_help

class PuzzleGUI:
    def __init__(self, master):
        self.master = master
        master.title("Open Source Spelling Bee Puzzle")

        # Initialize current score and remaining words
        self.current_score = 0
        self.remaining_words = 0

        self.setup()

    def setup(self):
        # Add GUI elements here
        self.welcome_label = tk.Label(self.master, text="Welcome to the Open Source Spelling Bee Puzzle!")
        self.welcome_label.pack()

        # Display honeycomb
        self.letters_label = tk.Label(self.master, text="Letters:")
        self.letters_label.pack()
        self.honeycomb_label = tk.Label(self.master, text="")
        self.honeycomb_label.pack()

        # Display scores
        self.scores_label = tk.Label(self.master, text="Max Score: 0\nCurrent Score: 0\nRemaining Words: 0")
        self.scores_label.pack()

        # Response box
        self.response_label = tk.Label(self.master, text="Your Guess:")
        self.response_label.pack()
        self.response_entry = tk.Entry(self.master)
        self.response_entry.pack()

        # Bind the <Return> key to handle input
        self.response_entry.bind("<Return>", self.submit_guess)

        # Quit button
        self.quit_button = tk.Button(self.master, text="Quit", command=self.master.quit)
        self.quit_button.pack()

        # Load puzzle
        self.load_puzzle()

    def load_puzzle(self):
        # Load puzzle logic here
        try:
            puzzle_idx = sys.argv[1].strip().upper()
        except:
            puzzle_idx = None

        if puzzle_idx is not None:
            utils.check_letters(puzzle_idx)
            puzzle_idx = utils.sort_letters(puzzle_idx)

        puzl_path = utils.select_puzzle(puzzle_idx)

        puzl = utils.read_puzzle(puzl_path)

        letters = puzl.get("letters")
        self.honeycomb_label.config(text=draw_letters_honeycomb(letters))

        self.total_score = puzl.get("total_score") + 7 * int(puzl.get("pangram_count"))
        self.word_count = puzl.get("word_count")
        self.remaining_words = self.word_count

        self.update_scores()

    def submit_guess(self, event):
        guess = self.response_entry.get().strip().upper()
        self.response_entry.delete(0, tk.END)

        # Handle the guess
        self.handle_guess(guess)

    def handle_guess(self, guess):
        # Implement the logic for checking the guess and updating the scores
        # Sample logic is provided here, you may need to replace it with your actual logic
        feedback = ""
        if len(guess) < 4:
            feedback = f"Guessed word is too short. Minimum length: 4"
        elif guess in valid_combinations:
            feedback = f"Your guess: {guess}\n✓ {guess}(guessed)\tword score = 1\twords found = 1/{self.word_count}\ttotal score = {self.current_score}/{self.total_score}"
            # Update scores
            self.current_score += 1
            self.remaining_words -= 1
            self.update_scores()
        else:
            feedback = f"Your guess: {guess}\nSorry, {guess} is not a valid word"

        self.show_feedback(feedback)

    def show_feedback(self, feedback):
        messagebox.showinfo("Feedback", feedback)
        # Schedule the removal of the message after 10 seconds
        self.master.after(10000, self.remove_feedback)

    def remove_feedback(self):
        # Close the feedback message
        self.master.update_idletasks()
        for w in self.master.winfo_children():
            if w.winfo_class() == 'Toplevel':
                w.destroy()

    def update_scores(self):
        self.scores_label.config(text=f"Max Score: {self.total_score}\nCurrent Score: {self.current_score}\nRemaining Words: {self.remaining_words}")

def main():
    root = tk.Tk()
    app = PuzzleGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
