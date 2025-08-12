# PyWord — a tiny Wordle-like terminal game (written in Python)

Guess a hidden **5-letter word** in **6 tries** right in your terminal. No external libraries. Quick to read, easy to hack.

## Features
- 🎯 Wordle-style feedback: **green** (correct spot), **yellow** (present elsewhere), **gray** (absent).
- ⌨️ Mini on-screen keyboard that tracks what you’ve learned.
- 🖥️ Works in any terminal; uses ANSI colors when available, graceful fallback otherwise.
- 🔧 Tiny codebase (single file), simple to customize.

## Demo
```
=== PyWord: a tiny Wordle-like game ===

Guess the 5-letter word! You have 6 tries.
Type your guess and press Enter. Type 'quit' to exit.

Attempt 1/6: crate
  C  [Y]  A  [G]  T
Keyboard:
  Q W E R T Y U I O P
  A S D F G H J K L
  Z X C V B N M

...
```

> Note: If your terminal doesn’t support ANSI colors, you’ll see tags like `[G]` (green), `[Y]` (yellow), and `[-]` (absent) next to letters. Gameplay is identical.

## Requirements
- Python **3.8+**
- No third‑party packages needed

## Installation & Run
1. Save the game file as `pyword.py` (use the code from the chat).
2. From the same folder, run:
   ```bash
   python pyword.py
   ```
3. Follow the on-screen prompts.

## How to Play
- Enter any **5-letter** alphabetical word, press **Enter**.
- Feedback per letter:
  - **Green**: right letter, right position.
  - **Yellow**: letter exists in the word, different position.
  - **Gray**: letter not in the word.
- The mini keyboard shows your best-known info per letter (green > yellow > gray).

## Configuration
Open the file and tweak the constants at the top:
```python
WORD_LENGTH = 5      # change length if you expand the word list accordingly
MAX_TRIES = 6        # increase/decrease difficulty
WORDS = [ ... ]      # add/remove words here
```
- If you change `WORD_LENGTH`, make sure every word in `WORDS` matches the new length.
- Add more words by extending the `WORDS` list (all lowercase).

## How duplicates are handled
The `score_guess()` function properly handles repeated letters. For example, if the target has a single `'A'` but your guess has two `'A'`s, only one of them can be marked green/yellow; the extra `'A'` will be gray.

## Tips
- On Windows Terminal / Windows 10+ terminals, ANSI colors are usually enabled by default. If colors don’t show, the game automatically falls back to tag-style markers.
- Type `quit` to exit mid-round.

## Roadmap ideas (nice-to-haves)
- Load words from an external `words.txt` file.
- Per-letter hard mode (all revealed hints must be used).
- Daily puzzle seed.
- Stats (win streaks, distribution).

## Acknowledgments
Inspired by **Wordle** (originally by Josh Wardle). This project is a learning exercise and not affiliated with The New York Times.

---

Happy hacking & have fun!
