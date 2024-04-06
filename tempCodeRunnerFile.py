import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from functools import partial
import threading

import play_puzzle
import utils
import params

class PuzzleGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Open Source Spelling Bee Puzzle")
        self.geometry("600x500")  # Adjusted dimensions for a 12-inch screen
        self.configure(bg="#F5F5F5")  # Light gray background

        self.current_puzzle = None
        self.guess_list = []

        self.create_widgets()

    def create_widgets(self):
        # Main Frame
        main_frame = tk.Frame(self, bg="#F5F5F5")
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Puzzle Display Frame
        self.puzzle_frame = tk.Frame(main_frame, bg="#FFFFFF", padx=20, pady=20)  # White background
        self.puzzle_frame.pack(fill=tk.BOTH, expand=True)

        # Scrollbar
        self.scrollbar = ttk.Scrollbar(self.puzzle_frame, orient=tk.VERTICAL, style="Vertical.TScrollbar")
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Puzzle Display Canvas
        self.canvas = tk.Canvas(self.puzzle_frame, bg="#FFFFFF", yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar.config(command=self.canvas.yview)

        self.frame = tk.Frame(self.canvas, bg="#FFFFFF")
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")

        # Bind events for updating scrollbar and canvas size
        self.frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)

        # Bind mouse wheel event to scrollbar
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

        # Adjust row and column weights to make puzzle frame expandable
        self.puzzle_frame.grid_rowconfigure(0, weight=1)
        self.puzzle_frame.grid_columnconfigure(0, weight=1)

        # Welcome Label and Play Button
        welcome_label = tk.Label(self.frame, text="Welcome to Open Source Spelling Bee Puzzle!", font=("Helvetica", 16), bg="#FFFFFF")
        welcome_label.grid(row=0, column=0, columnspan=2, pady=(20, 10))

        play_button = tk.Button(self.frame, text="Play Puzzle", command=self.load_puzzle, font=("Helvetica", 12), bg="#FFA500", fg="#FFFFFF")
        play_button.grid(row=1, column=0, columnspan=2, pady=(0, 10), padx=10)

        # Current Puzzle Info
        self.info_label = tk.Label(self.frame, text="", font=("Helvetica", 12), bg="#FFFFFF")
        self.info_label.grid(row=2, column=0, columnspan=2, pady=(0, 10))

        # Guess Entry
        self.guess_entry = tk.Entry(self.frame, font=("Helvetica", 12))
        self.guess_entry.grid(row=3, column=0, columnspan=2, pady=(0, 10))

        # Submit Guess Button
        submit_guess = partial(self.submit_guess)
        submit_button = tk.Button(self.frame, text="Submit Guess", command=submit_guess, font=("Helvetica", 12), bg="#FFA500", fg="#FFFFFF")
        submit_button.grid(row=4, column=0, columnspan=2, pady=(0, 10))

    def on_frame_configure(self, event):
        """Reset the scroll region to encompass the inner frame"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event):
        """Update the scroll region to fit the canvas size"""
        self.canvas.itemconfig(self.frame, width=event.width)

    def on_mousewheel(self, event):
        """Scroll the scrollbar with mouse wheel event"""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def load_puzzle(self):
        puzzle_idx = None  # Since you want to load a random puzzle
        puzzle_path = utils.select_puzzle(puzzle_idx)
        self.current_puzzle = utils.read_puzzle(puzzle_path)
        self.guess_list = []

        letters = self.current_puzzle.get("letters")
        honeycomb = play_puzzle.draw_letters_honeycomb(letters)
        self.info_label.config(text=f"Playing puzzle index: {letters}\nYour letters are:\n{honeycomb}\nMax score: {self.current_puzzle.get('total_score')}\nTotal words: {self.current_puzzle.get('word_count')}")

        # Start a new thread to run the quiz
        threading.Thread(target=self.run_quiz).start()

    def run_quiz(self):
        while True:
            guess = input("Your guess: ").strip().upper()
            if guess == "!Q":
                break
            elif guess == "!H":
                play_puzzle.get_hint(self.current_puzzle, self.guess_list)
            else:
                self.check_guess(guess)

    def submit_guess(self):
        if not self.current_puzzle:
            messagebox.showwarning("Warning", "Please load a puzzle first!")
            return

        guess = self.guess_entry.get().strip().upper()
        self.guess_entry.delete(0, tk.END)

        if guess.startswith("!"):
            if guess == "!Q":
                return
            elif guess == "!H":
                play_puzzle.get_hint(self.current_puzzle, self.guess_list)
                return

        self.check_guess(guess)

    def check_guess(self, guess):
        if guess in self.guess_list:
            messagebox.showwarning("Duplicate", f"You already found: {guess}")
            return

        if not play_puzzle.is_valid_word(guess, self.current_puzzle):
            messagebox.showwarning("Invalid Word", f"Sorry, {guess} is not a valid word")
            return

        if not play_puzzle.is_word_possible(guess, self.current_puzzle["letters"]):
            messagebox.showwarning("Invalid Guess", f"Sorry, {guess} cannot be formed from the given letters")
            return

        if not play_puzzle.is_word_unique(guess, self.guess_list):
            messagebox.showwarning("Duplicate", f"You already found {guess}")
            return

        score = play_puzzle.calculate_score(guess, self.current_puzzle["letters"])
        self.guess_list.append(guess)
        messagebox.showinfo("Correct Guess", f"Congratulations! You found {guess}.\nYour score: {score}")

if __name__ == "__main__":
    app = PuzzleGUI()
    app.mainloop()
