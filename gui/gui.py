import tkinter as tk
import random

# ---------------- Global Variables ----------------
total_score = 0

# ---------------- Load Chains ----------------
def load_chains(filename="data/word_chain.txt"):
    chains = []
    with open(filename, "r") as f:
        for line in f:
            words = [w.strip() for w in line.strip().split(",")]
            if words:
                chains.append(words)
    return chains

# ---------------- Word Chain Game Class ----------------
class WordChainGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Word Chain Game")
        self.master.geometry("900x900")
        self.master.resizable(True, True)

        self.chains = load_chains()
        random.shuffle(self.chains)

        self.cell_labels = []  # 2D list: rows=words, cols=letters
        self.editable = []     # 2D list: which cells are editable

        self.init_main_menu()

    # ---------------- Main Menu ----------------
    def init_main_menu(self):
        global total_score
        total_score = 0            # Reset total score when returning to menu
        self.session_score = 0     # Reset session score

        self.clear_window()
        title = tk.Label(self.master, text="WORD CHAIN GAME", font=("Helvetica", 32, "bold"))
        title.pack(pady=50)

        normal_btn = tk.Button(self.master, text="Normal Mode", font=("Helvetica", 20), width=20,
                               command=lambda: self.start_game("normal"))
        normal_btn.pack(pady=20)

        hard_btn = tk.Button(self.master, text="Hard Mode", font=("Helvetica", 20), width=20,
                             command=lambda: self.start_game("hard"))
        hard_btn.pack(pady=20)

        quit_btn = tk.Button(self.master, text="Quit", font=("Helvetica", 16), width=10,
                             command=self.master.quit)
        quit_btn.pack(pady=50)

    # ---------------- Utility ----------------
    def clear_window(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    # ---------------- Game Initialization ----------------
    def start_game(self, difficulty):
        self.difficulty = difficulty
        self.session_score = 0
        self.chain_index = 0
        random.shuffle(self.chains)
        self.load_game_ui()
        self.load_chain()
        self.master.focus_set()
        self.master.bind("<Key>", self.on_keypress)
        self.chain_failed = False


    # ---------------- Game UI ----------------
    def load_game_ui(self):
        self.clear_window()

        # Scrollable frame
        canvas = tk.Canvas(self.master, height=500)
        scrollbar = tk.Scrollbar(self.master, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.grid_frame = tk.Frame(self.scrollable_frame)
        self.grid_frame.pack(pady=20)

        self.feedback_label = tk.Label(self.scrollable_frame, text="", font=("Helvetica", 16))
        self.feedback_label.pack(pady=5)

        self.hint_button = tk.Button(self.scrollable_frame, text="Hint (-10 pts)", font=("Helvetica", 16),
                                     command=self.use_hint)
        self.hint_button.pack(pady=5)

        self.score_label = tk.Label(self.scrollable_frame, text=f"Session Score: 0 | Total Score: {total_score}",
                                    font=("Helvetica", 16))
        self.score_label.pack(pady=20)

        self.menu_button = tk.Button(self.scrollable_frame, text="Return to Main Menu", font=("Helvetica", 16),
                                     command=self.init_main_menu)
        self.menu_button.pack(pady=10)

    # ---------------- Feedback ----------------
    def show_feedback(self, message, color="red", duration=2000):
        self.feedback_label.config(text=message, fg=color)
        self.master.after(duration, lambda: self.feedback_label.config(text=""))

    # ---------------- Chain Handling ----------------
    def load_chain(self):
        if self.chain_index >= len(self.chains):
            self.show_feedback(f"End of all chains! Session Score: {self.session_score} | Total Score: {total_score}", "blue", 5000)
            return

        self.current_chain = self.chains[self.chain_index]
        self.chain_index += 1
        self.word_index = 1         # start after first word
        self.current_letter_index = 1
        self.word_score = 100
        self.attempts_left = 4

        # Clear previous grid
        for row in self.cell_labels:
            for lbl in row:
                lbl.destroy()
        self.cell_labels.clear()
        self.editable.clear()

        # Create Wordle-style boxes
        for r, word in enumerate(self.current_chain):
            row_labels = []
            row_editable = []
            for c, letter in enumerate(word):
                if r == 0:
                    lbl = tk.Label(self.grid_frame, text=letter.upper(), font=("Helvetica", 24),
                                   width=4, height=2, bg="white", relief="solid")
                    row_editable.append(False)
                else:
                    if c == 0:
                        lbl = tk.Label(self.grid_frame, text=letter.upper(), font=("Helvetica", 24),
                                       width=4, height=2, bg="white", relief="solid")
                        row_editable.append(False)
                    else:
                        lbl = tk.Label(self.grid_frame, text="", font=("Helvetica", 24),
                                       width=4, height=2, bg="white", relief="solid")
                        row_editable.append(True)
                lbl.grid(row=r, column=c, padx=5, pady=5)
                row_labels.append(lbl)
            self.cell_labels.append(row_labels)
            self.editable.append(row_editable)

    # ---------------- Hint Logic ----------------
    def use_hint(self):
        if self.difficulty == "hard":
            return

        word = self.current_chain[self.word_index]
        labels = self.cell_labels[self.word_index]
        editable_row = self.editable[self.word_index]

        hint_used = False
        for i, can_edit in enumerate(editable_row):
            if can_edit and labels[i].cget("text") == "":
                labels[i].config(text=word[i].upper(), bg="yellow")
                editable_row[i] = False
                self.word_score -= 10
                self.current_letter_index = i + 1
                hint_used = True
                self.show_feedback("Hint used! -10 points", "orange")
                break

        if not hint_used:
            self.show_feedback("All hints used! No points for this word", "gray")

        # After hint, check if word fully revealed
        if all(lbl.cget("text") != "" for i, lbl in enumerate(labels) if not editable_row[i]):
            self.check_word_completion()

    # ---------------- Keypress Handling ----------------
    def on_keypress(self, event):
        key = event.char.upper()

        if key == '\x08':  # Backspace
            self.handle_backspace()
            return

        if not key.isalpha():
            return

        word = self.current_chain[self.word_index]
        labels = self.cell_labels[self.word_index]
        editable_row = self.editable[self.word_index]

        # Find next editable cell
        while self.current_letter_index < len(word) and not editable_row[self.current_letter_index]:
            self.current_letter_index += 1
        if self.current_letter_index >= len(word):
            return

        lbl = labels[self.current_letter_index]
        lbl.config(text=key, bg="white")
        self.current_letter_index += 1

        # Check completion
        if all(lbl.cget("text") != "" for i, lbl in enumerate(labels) if editable_row[i]):
            self.check_word_completion()

    # ---------------- Handle Backspace ----------------
    def handle_backspace(self):
        labels = self.cell_labels[self.word_index]
        editable_row = self.editable[self.word_index]

        i = self.current_letter_index - 1
        while i >= 0 and not editable_row[i]:
            i -= 1
        if i >= 0:
            labels[i].config(text="", bg="white")
            self.current_letter_index = i

    # ---------------- Word Completion ----------------
    def check_word_completion(self):
        global total_score
        labels = self.cell_labels[self.word_index]
        word = self.current_chain[self.word_index]
        typed = "".join(lbl.cget("text") if lbl.cget("text") != "" else "_" for lbl in labels).lower()

    #------Hard mode -------------
        if self.difficulty == "hard":
            if typed == word.lower():
            # Turn all boxes green
                for lbl in labels:
                    lbl.config(bg="green")
                points = 100
                total_score += points
                self.session_score += points
                self.show_feedback(f"✅ Correct! +{points} points", "green")

                # Move to next word
                self.word_index += 1
                if self.word_index >= len(self.current_chain):
                    # Chain complete
                    self.load_chain()
                else:
                    self.current_letter_index = 1
            else:
                # Wrong word → reset entire chain
                for i, lbl in enumerate(labels):
                    if self.editable[self.word_index][i]:
                        lbl.config(text=word[i].upper(), bg="red")
                self.show_feedback(f"❌ Wrong! Chain reset!", "red")
                # Select a new random chain
                self.load_chain()
            self.score_label.config(text=f"Session Score: {self.session_score} | Total Score: {total_score}")
            return  # exit early, skip normal mode logic

    #------NORMAL MODE ------------
        # Count letters revealed by hint
        revealed_by_hint = sum(1 for i, lbl in enumerate(labels) 
                               if lbl.cget("bg") == "yellow" and self.editable[self.word_index][i])
        total_editable = sum(self.editable[self.word_index])

        # Word typed correctly
        if typed == word.lower():
            if revealed_by_hint == total_editable:
                # All hints used → no points
                points = 0
                self.show_feedback("All hints used! No points for this word", "gray")
                for i, lbl in enumerate(labels):
                    if lbl.cget("bg") == "yellow":
                        lbl.config(bg="yellow")
            else:
                # Deduct 10 points per hint used
                points = self.word_score - (revealed_by_hint * 10)
                total_score += points
                self.session_score += points
                for lbl in labels:
                    if lbl.cget("bg") != "yellow":
                        lbl.config(bg="green")
                self.show_feedback(f"✅ Correct! +{points} points", "green")

            # Move to next word
            self.word_index += 1
            if self.word_index >= len(self.current_chain):
                if self.difficulty == "normal" and not self.chain_failed:
                    total_score += 50
                    self.session_score += 50
                    self.show_feedback("🎉 Chain completed! Bonus +50 points", "blue")
                self.load_chain()
            else:
                self.current_letter_index = 1
                self.word_score = 100
                self.attempts_left = 3

        # Word typed incorrectly
        else:
            self.attempts_left -= 1
            if self.attempts_left > 0:
                self.show_feedback(f"{self.attempts_left} attempts left", "red")
            else:
                # Reveal all letters in red for failed word
                for i, lbl in enumerate(labels):
                    if self.editable[self.word_index][i]:
                        lbl.config(text=word[i].upper(), bg="red")
                self.chain_failed = True

                self.show_feedback(f"🚫 Out of chances! The word was '{word}'", "red")

                # Move to next word or chain
                self.word_index += 1
                if self.word_index >= len(self.current_chain):
                    self.load_chain()
                else:
                    self.current_letter_index = 1
                    self.word_score = 100
                    self.attempts_left = 3

        # Update score display
        self.score_label.config(text=f"Session Score: {self.session_score} | Total Score: {total_score}")

# ---------------- Run GUI ----------------
root = tk.Tk()
game = WordChainGame(root)
root.mainloop()
