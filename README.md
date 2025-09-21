# word-chain-game-gui
A fun, interactive word puzzle game built in Python with a Tkinter GUI, inspired by games like Wordle but with a unique twist.  In this game, you complete a chain of connected words, where each word leads to the next. You’ll need logic, vocabulary, and a bit of luck to succeed

**How the Game Works**

The game starts with a word chain (e.g., golf → club → card → game).
The first word is revealed, and you must guess each following word, letter by letter.
You type letters into boxes (like Wordle style).
**Normal Mode:**
You get 3 attempts per word.
You can use hints (reveals letters) at a cost of points.
Points per correct word: 100 max, minus 10 per hint.
No points if all letters are revealed by hints.
Bonus: +50 points if you complete the entire chain without mistakes.

**Hard Mode:**
No hints, no retries.
One mistake resets the entire chain with a new one.

**Features**
Clean Tkinter GUI with a grid-based interface (similar to Wordle).
Real-time feedback:
✅ Green for correct words.
🟨 Yellow for hinted letters.
❌ Red when attempts are used up.
Session scoring + total score across multiple games.
Two difficulty modes: Normal & Hard.
Scrollable game area for long word chains.
Option to return to the main menu.

**Skills & Technologies**
This project highlights:
Python 3
Tkinter (GUI development, grid layouts, scrollable frames)
OOP (Object-Oriented Programming) for clean game logic
Game logic design: word chains, hint system, scoring system, difficulty modes
Problem solving & debugging complex state management
Git & GitHub for version control

**Run Game GUI**
python -m gui.gui

**Run game terminal - Normal only**
python main.py
