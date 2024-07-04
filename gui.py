import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from functools import partial
import utils
import play_puzzle

class PuzzleGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Spelling Bee Puzzle")
        self.configure(bg="#F5F5F5")  # Light gray background

        self.current_puzzle = None
        self.guess_list = []

        self.create_widgets()

    def create_widgets(self):
        # Get screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate inner window dimensions
        inner_width = int(screen_width * 0.8)
        inner_height = int(screen_height * 0.8)

        # Set window dimensions to fit the screen
        self.geometry(f"{inner_width}x{inner_height}+{int((screen_width - inner_width) / 2)}+{int((screen_height - inner_height) / 2)}")

        # Main Frame
        main_frame = tk.Frame(self, bg="#F5F5F5")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Puzzle Display Frame
        self.puzzle_frame = tk.Frame(main_frame, bg="#0074D9", padx=40, pady=40)  # White background
        self.puzzle_frame.pack(fill=tk.BOTH, expand=True)

        # Puzzle Display Canvas
        self.canvas = tk.Canvas(self.puzzle_frame, bg="#FFFFFF")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = ttk.Scrollbar(self.puzzle_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.frame = tk.Frame(self.canvas, bg="#FFFFFF")
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")

        # Bind events for updating scrollbar and canvas size
        self.frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)

        # Bind mouse wheel event to scrollbar
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

        # Welcome Label and Play Button
        welcome_label = tk.Label(self.frame, text="Welcome to Spelling Bee Puzzle!", font=("Helvetica", 16), bg="#FFFFFF", fg="#FFA500")  # White background with orange text
        welcome_label.grid(row=0, column=0, columnspan=2, pady=(inner_height // 4, 40), padx=(inner_width // 4, inner_width // 4), sticky="nsew")  # Centered vertically and horizontally

        play_button = tk.Button(self.frame, text="Play Puzzle", command=self.load_puzzle, font=("Helvetica", 12), bg="#FFA500", fg="#FFFFFF")  # Orange button with white text
        play_button.grid(row=1, column=0, pady=(0, 20), padx=(20, 10), sticky="nsew")

        exit_button = tk.Button(self.frame, text="Exit", command=self.quit, font=("Helvetica", 12), bg="#FFA500", fg="#FFFFFF")  # Orange button with white text
        exit_button.grid(row=1, column=1, pady=(0, 20), padx=(10, 20), sticky="nsew")
        
    def on_frame_configure(self, event):
        """Reset the scroll region to encompass the inner frame"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event):
        """Update the scroll region to fit the canvas size"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

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
        self.info_label = tk.Label(self.frame, text=f"Playing puzzle index: {letters}\nYour letters are:\n{honeycomb}\nMax score: {self.current_puzzle.get('total_score')}\n\nTotal words: {self.current_puzzle.get('word_count')}", font=("Helvetica", 12), bg="#FFFFFF")
        self.info_label.grid(row=2, column=0, columnspan=2, pady=(0, 10))

        # Player Score Label
        self.player_score_label = tk.Label(self.frame, text="Player Score: 0", font=("Helvetica", 12), bg="#FFFFFF")
        self.player_score_label.grid(row=3, column=0, columnspan=2, pady=(0, 10))

        # Player Words Guessed Label
        self.player_words_label = tk.Label(self.frame, text="Player Words Guessed: 0", font=("Helvetica", 12), bg="#FFFFFF")
        self.player_words_label.grid(row=4, column=0, columnspan=2, pady=(0, 10))

        # Pangram Found Label
        self.pangram_found_label = tk.Label(self.frame, text="Pangram Found: False", font=("Helvetica", 12), bg="#FFFFFF")
        self.pangram_found_label.grid(row=5, column=0, columnspan=2, pady=(0, 10))

        # Guess Entry
        self.guess_entry = tk.Entry(self.frame, font=("Helvetica", 12))
        self.guess_entry.grid(row=6, column=0, columnspan=2, pady=(0, 10))
        self.guess_entry.bind("<Return>", lambda event: self.submit_guess())  # Bind Enter key event

        # Submit Guess Button
        submit_guess = partial(self.submit_guess)
        submit_button = tk.Button(self.frame, text="Submit Guess", command=submit_guess, font=("Helvetica", 12), bg="#FFA500", fg="#FFFFFF")
        submit_button.grid(row=7, column=0, columnspan=2, pady=(0, 10))

        # Help Button
        help_button = tk.Button(self.frame, text="Help", command=self.show_help_window, font=("Helvetica", 12), bg="#FFA500", fg="#FFFFFF")
        help_button.grid(row=8, column=0, columnspan=2, pady=(0, 10))

    def show_help_window(self):
        help_window = tk.Toplevel(self)
        help_window.title("Help")
        help_window.geometry("300x150")
        help_window.configure(bg="#0074D9")  # Blue background

        # Instructions Button
        instructions_button = tk.Button(help_window, text="Instructions", command=self.show_instructions, font=("Helvetica", 12), bg="#FFA500", fg="#FFFFFF")
        instructions_button.pack(side=tk.TOP, pady=10)

        # Show Answers Button
        show_answers_button = tk.Button(help_window, text="Show Answers", command=self.show_answers_window, font=("Helvetica", 12), bg="#FFA500", fg="#FFFFFF")
        show_answers_button.pack(side=tk.TOP, pady=10)

        # Back Button
        back_button = tk.Button(help_window, text="Close Help", command=help_window.destroy, font=("Helvetica", 12), bg="#FFA500", fg="#FFFFFF")
        back_button.pack(side=tk.TOP, pady=10)

    def show_instructions(self):
        instructions_window = tk.Toplevel(self)
        instructions_window.title("Instructions")
        instructions_window.geometry("400x400")
        instructions_window.configure(bg="##0074D9")  # Blue background

        # Instructions Text
        instructions = play_puzzle.get_instructions()
        instructions_text = scrolledtext.ScrolledText(instructions_window, wrap=tk.WORD, width=40, height=10, font=("Helvetica", 12))
        instructions_text.insert(tk.END, instructions)
        instructions_text.pack(expand=True, fill="both")

        # Back Button
        back_button = tk.Button(instructions_window, text="Back", command=instructions_window.destroy, font=("Helvetica", 12), bg="#FFA500", fg="#FFFFFF")
        back_button.pack(side=tk.BOTTOM, pady=10)

    def show_answers_window(self):
        answers_window = tk.Toplevel(self)
        answers_window.title("Answers")
        answers_window.geometry("400x400")
        answers_window.configure(bg="#0074D9")  # Blue background

        # Sort word list based on length
        word_list = self.current_puzzle.get("word_list")
        sorted_word_list = sorted(word_list, key=lambda x: len(x["word"]))

        # Group words by length and count the number of words for each length
        word_count = {}
        for word_entry in sorted_word_list:
            word_length = len(word_entry["word"])
            if word_length not in word_count:
                word_count[word_length] = 0
            word_count[word_length] += 1

        # Display word counts
        answer_text = ""
        for length, count in sorted(word_count.items()):
            answer_text += f"{length} letters words: {count}\n"

        answer_text_widget = scrolledtext.ScrolledText(answers_window, wrap=tk.WORD, width=40, height=10, font=("Helvetica", 12))
        answer_text_widget.insert(tk.END, answer_text)
        answer_text_widget.pack(expand=True, fill="both")

        # Back Button
        back_button = tk.Button(answers_window, text="Back", command=answers_window.destroy, font=("Helvetica", 12), bg="#FFA500", fg="#FFFFFF")
        back_button.pack(side=tk.BOTTOM, pady=10)

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
            elif guess == "!I":
                instructions = play_puzzle.get_instructions()
                messagebox.showinfo("Instructions", instructions)
                return
            elif guess == "!F":
                play_puzzle.shuffle_letters(self.current_puzzle)
                self.load_puzzle()  # Reload puzzle after shuffling
                return
            elif guess == "!A":
                self.show_answers_window()
                return

        self.check_guess(guess)

    import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from functools import partial
import utils
import play_puzzle

class PuzzleGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Spelling Bee Puzzle")
        self.configure(bg="#F5F5F5")  # Light gray background

        self.current_puzzle = None
        self.guess_list = []

        self.create_widgets()

    def create_widgets(self):
        # Get screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate inner window dimensions
        inner_width = int(screen_width * 0.8)
        inner_height = int(screen_height * 0.8)

        # Set window dimensions to fit the screen
        self.geometry(f"{inner_width}x{inner_height}+{int((screen_width - inner_width) / 2)}+{int((screen_height - inner_height) / 2)}")

        # Main Frame
        main_frame = tk.Frame(self, bg="#F5F5F5")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Puzzle Display Frame
        self.puzzle_frame = tk.Frame(main_frame, bg="#0074D9", padx=40, pady=40)  # Blue background
        self.puzzle_frame.pack(fill=tk.BOTH, expand=True)

        # Puzzle Display Canvas
        self.canvas = tk.Canvas(self.puzzle_frame, bg="#FFFFFF")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = ttk.Scrollbar(self.puzzle_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.frame = tk.Frame(self.canvas, bg="#FFFFFF")
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")

        # Bind events for updating scrollbar and canvas size
        self.frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)

        # Bind mouse wheel event to scrollbar
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

        # Welcome Label and Play Button
        welcome_label = tk.Label(self.frame, text="Welcome to Spelling Bee Puzzle!", font=("Helvetica", 16), bg="#FFFFFF", fg="#FFA500")  # White background with orange text
        welcome_label.grid(row=0, column=0, columnspan=2, pady=(inner_height // 4, 40), padx=(inner_width // 4, inner_width // 4), sticky="nsew")  # Centered vertically and horizontally

        play_button = tk.Button(self.frame, text="Play Puzzle", command=self.load_puzzle, font=("Helvetica", 12), bg="#FFA500", fg="#FFFFFF")  # Orange button with white text
        play_button.grid(row=1, column=0, pady=(0, 20), padx=(20, 10), sticky="nsew")

        exit_button = tk.Button(self.frame, text="Exit", command=self.quit, font=("Helvetica", 12), bg="#FFA500", fg="#FFFFFF")  # Orange button with white text
        exit_button.grid(row=1, column=1, pady=(0, 20), padx=(10, 20), sticky="nsew")
        
    def on_frame_configure(self, event):
        """Reset the scroll region to encompass the inner frame"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event):
        """Update the scroll region to fit the canvas size"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

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
        self.info_label = tk.Label(self.frame, text=f"Playing puzzle index: {letters}\nYour letters are:\n{honeycomb}\nMax score: {self.current_puzzle.get('total_score')}\n\nTotal words: {self.current_puzzle.get('word_count')}", font=("Helvetica", 12), bg="#FFFFFF")
        self.info_label.grid(row=2, column=0, columnspan=2, pady=(0, 10))

        # Player Score Label
        self.player_score_label = tk.Label(self.frame, text="Player Score: 0", font=("Helvetica", 12), bg="#FFFFFF")
        self.player_score_label.grid(row=3, column=0, columnspan=2, pady=(0, 10))

        # Player Words Guessed Label
        self.player_words_label = tk.Label(self.frame, text="Player Words Guessed: 0", font=("Helvetica", 12), bg="#FFFFFF")
        self.player_words_label.grid(row=4, column=0, columnspan=2, pady=(0, 10))

        # Pangram Found Label
        self.pangram_found_label = tk.Label(self.frame, text="Pangram Found: False", font=("Helvetica", 12), bg="#FFFFFF")
        self.pangram_found_label.grid(row=5, column=0, columnspan=2, pady=(0, 10))

        # Guess Entry
        self.guess_entry = tk.Entry(self.frame, font=("Helvetica", 12))
        self.guess_entry.grid(row=6, column=0, columnspan=2, pady=(0, 10))
        self.guess_entry.bind("<Return>", lambda event: self.submit_guess())  # Bind Enter key event

        # Submit Guess Button
        submit_guess = partial(self.submit_guess)
        submit_button = tk.Button(self.frame, text="Submit Guess", command=submit_guess, font=("Helvetica", 12), bg="#FFA500", fg="#FFFFFF")
        submit_button.grid(row=7, column=0, columnspan=2, pady=(0, 10))

        # Help Button
        help_button = tk.Button(self.frame, text="Help", command=self.show_help_window, font=("Helvetica", 12), bg="#FFA500", fg="#FFFFFF")
        help_button.grid(row=8, column=0, columnspan=2, pady=(0, 10))

    def show_help_window(self):
        help_window = tk.Toplevel(self)
        help_window.title("Help")
        help_window.geometry("300x150")
        help_window.configure(bg="#0074D9")  # Blue background

        # Instructions Button
        instructions_button = tk.Button(help_window, text="Instructions", command=self.show_instructions, font=("Helvetica", 12), bg="#FFA500", fg="#FFFFFF")
        instructions_button.pack(side=tk.TOP, pady=10)

        # Show Answers Button
        show_answers_button = tk.Button(help_window, text="Show Answers", command=self.show_answers_window, font=("Helvetica", 12), bg="#FFA500", fg="#FFFFFF")
        show_answers_button.pack(side=tk.TOP, pady=10)

        # Back Button
        back_button = tk.Button(help_window, text="Close Help", command=help_window.destroy, font=("Helvetica", 12), bg="#FFA500", fg="#FFFFFF")
        back_button.pack(side=tk.TOP, pady=10)

    def show_instructions(self):
        instructions_window = tk.Toplevel(self)
        instructions_window.title("Instructions")
        instructions_window.geometry("400x400")
        instructions_window.configure(bg="#0074D9")  # Blue background

        # Instructions Text
        instructions = play_puzzle.get_instructions()
        instructions_text = scrolledtext.ScrolledText(instructions_window, wrap=tk.WORD, width=40, height=10, font=("Helvetica", 12))
        instructions_text.insert(tk.END, instructions)
        instructions_text.pack(expand=True, fill="both")

        # Back Button
        back_button = tk.Button(instructions_window, text="Back", command=instructions_window.destroy, font=("Helvetica", 12), bg="#FFA500", fg="#FFFFFF")
        back_button.pack(side=tk.BOTTOM, pady=10)

    def show_answers_window(self):
        answers_window = tk.Toplevel(self)
        answers_window.title("Answers")
        answers_window.geometry("400x400")
        answers_window.configure(bg="#0074D9")  # Blue background

        # Sort word list based on length
        word_list = self.current_puzzle.get("word_list")
        sorted_word_list = sorted(word_list, key=lambda x: len(x["word"]))

        # Group words by length and count the number of words for each length
        word_count = {}
        for word_entry in sorted_word_list:
            word_length = len(word_entry["word"])
            if word_length not in word_count:
                word_count[word_length] = 0
            word_count[word_length] += 1

        # Display word counts
        answer_text = ""
        for length, count in sorted(word_count.items()):
            answer_text += f"{length} letters words: {count}\n"

        answer_text_widget = scrolledtext.ScrolledText(answers_window, wrap=tk.WORD, width=40, height=10, font=("Helvetica", 12))
        answer_text_widget.insert(tk.END, answer_text)
        answer_text_widget.pack(expand=True, fill="both")

        # Back Button
        back_button = tk.Button(answers_window, text="Back", command=answers_window.destroy, font=("Helvetica", 12), bg="#FFA500", fg="#FFFFFF")
        back_button.pack(side=tk.BOTTOM, pady=10)
        
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
            elif guess == "!I":
                instructions = play_puzzle.get_instructions()
                messagebox.showinfo("Instructions", instructions)
                return
            elif guess == "!F":
                play_puzzle.shuffle_letters(self.current_puzzle)
                self.load_puzzle()  # Reload puzzle after shuffling
                return
            elif guess == "!A":
                self.show_answers_window()
                return

        self.check_guess(guess)

    def check_guess(self, guess):
        if guess in self.guess_list:
            messagebox.showwarning("Duplicate", f"You already found: {guess}")
            return

        # Check if the guess is in the word list of the current puzzle
        # Update the key to "word_list"
        if guess not in [word["word"] for word in self.current_puzzle["word_list"]]:
            messagebox.showwarning("Invalid Word", f"Sorry, {guess} is not a valid word")
            return

        # Check if the guess can be formed from the given letters
        if not play_puzzle.is_word_possible(guess, self.current_puzzle["letters"]):
            messagebox.showwarning("Invalid Guess", f"Sorry, {guess} cannot be formed from the given letters")
            return

        # Initialize pangram_found to False
        pangram_found = True

        # Check if the key 'player_pangram' exists in the current_puzzle dictionary
        if "player_pangram" in self.current_puzzle:
            pangram_found = self.current_puzzle["player_pangram"]

        # Calculate score and update labels
        score = play_puzzle.calculate_score(guess, self.current_puzzle["letters"])
        self.player_score_label.config(text=f"Player Score: {score}")
        self.player_words_label.config(text=f"Player Words Guessed: {len(self.guess_list) + 1}")

        # Check if pangram found and update label
        self.pangram_found_label.config(text=f"Pangram Found: {pangram_found}")

        # Update guess list and show message
        self.guess_list.append(guess)
        messagebox.showinfo("Correct Guess", f"Congratulations! You found {guess}.\nYour score: {score}")


if __name__ == "__main__":
    app = PuzzleGUI()
    app.mainloop()
