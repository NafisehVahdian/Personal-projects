import random
import sys
import string

# ========= Config =========
WORD_LENGTH = 5
MAX_TRIES = 6

# Small built-in word list (you can expand this)
WORDS = [
    "cigar","rebut","sissy","humph","awake","blush","focal","evade","naval","serve",
    "heath","dwarf","model","karma","stink","grade","quiet","bench","abate","feign",
    "major","death","fresh","crust","stool","colon","abase","marry","react","batty",
    "pride","floss","helix","croak","staff","paper","unfed","whelp","trawl","outdo",
    "adobe","crazy","sower","repay","digit","crate","cluck","spike","mimic","pound",
    "maxim","linen","unmet","flesh","booby","forth","first","stand","belly","ivory",
    "seedy","print","yearn","drain","bribe","stout","panel","crass","flume","offal",
    "agree","error","swirl","argue","bleed","delta","flick","totem","wooer","front",
    "shrub","parry","biome","lapel","start","greet","goner","golem","lusty","loopy",
    "round","audit","lying","gamma","labor","islet","civic","forge","corny","moult",
    "basic","salad","agate","spicy","spray","essay","fjord","spend","kebab","guild"
]

# ========= Helpers =========
def supports_ansi() -> bool:
    """Detect if terminal likely supports ANSI colors."""
    if sys.platform.startswith("win"):
        # Modern Windows terminals usually support ANSI; if not, fallback still works.
        return True
    return sys.stdout.isatty()

ANSI = supports_ansi()

def color_block(letter: str, status: str) -> str:
    """
    status in {"correct","present","absent"}.
    Prints a colored block with the letter.
    """
    if not ANSI:
        # Fallback: tag-style
        tag = {"correct":"[G]","present":"[Y]","absent":"[-]"}[status]
        return f"{letter.upper()}{tag}"
    # ANSI background colors: green/yellow/gray
    bg = {"correct":"\033[42m", "present":"\033[43m", "absent":"\033[47m"}[status]
    fg = "\033[30m"  # black text for contrast
    reset = "\033[0m"
    return f"{bg}{fg} {letter.upper()} {reset}"

def score_guess(target: str, guess: str):
    """
    Wordle-like scoring that handles duplicate letters correctly.
    Returns list of statuses: "correct", "present", "absent".
    """
    target = target.lower()
    guess = guess.lower()
    n = len(target)
    result = ["absent"] * n
    counts = {}

    # First pass: mark greens; count the rest
    for i in range(n):
        if guess[i] == target[i]:
            result[i] = "correct"
        else:
            counts[target[i]] = counts.get(target[i], 0) + 1

    # Second pass: mark yellows if available
    for i in range(n):
        if result[i] == "correct":
            continue
        ch = guess[i]
        if counts.get(ch, 0) > 0:
            result[i] = "present"
            counts[ch] -= 1
        else:
            result[i] = "absent"
    return result

def is_valid_guess(s: str) -> bool:
    return len(s) == WORD_LENGTH and all(c in string.ascii_letters for c in s)

def show_keyboard(letter_states):
    """
    Display a tiny keyboard with best-known statuses per letter.
    Priority: correct > present > absent > unknown.
    """
    rows = ["qwertyuiop", "asdfghjkl", "zxcvbnm"]
    def rank(state):
        return {"correct":3, "present":2, "absent":1, "unknown":0}.get(state, 0)

    lines = []
    for row in rows:
        parts = []
        for ch in row:
            st = letter_states.get(ch, "unknown")
            if st == "unknown":
                parts.append(ch.upper())
            else:
                parts.append(color_block(ch, st if st in {"correct","present","absent"} else "absent"))
        lines.append(" ".join(parts))
    print("\nKeyboard:")
    for ln in lines:
        print(" ", ln)
    print()

def merge_state(old, new):
    """Keep the strongest evidence for a letter (correct > present > absent > unknown)."""
    order = {"unknown":0,"absent":1,"present":2,"correct":3}
    return new if order[new] > order[old] else old

# ========= Game =========
def play_once():
    target = random.choice(WORDS).lower()
    letter_states = {}  # per-letter best state
    # Uncomment to debug:
    # print("(debug) Target:", target)

    print(f"\nGuess the {WORD_LENGTH}-letter word! You have {MAX_TRIES} tries.")
    print("Type your guess and press Enter. Type 'quit' to exit.\n")

    for attempt in range(1, MAX_TRIES + 1):
        while True:
            guess = input(f"Attempt {attempt}/{MAX_TRIES}: ").strip().lower()
            if guess == "quit":
                print("Bye!")
                return
            if is_valid_guess(guess):
                break
            print(f"Please enter a {WORD_LENGTH}-letter alphabetical word.")

        statuses = score_guess(target, guess)

        # Print colored feedback
        line = " ".join(color_block(ch, st) for ch, st in zip(guess, statuses))
        print(line)

        # Update keyboard states
        for ch, st in zip(guess, statuses):
            old = letter_states.get(ch, "unknown")
            letter_states[ch] = merge_state(old, st)

        show_keyboard(letter_states)

        if all(st == "correct" for st in statuses):
            print(f"Great job! You guessed it in {attempt} {'try' if attempt==1 else 'tries'} 🎉\n")
            return

    print(f"Out of tries! The word was: {target.upper()}\n")

def main():
    print("=== PyWord: a tiny Wordle-like game ===")
    while True:
        play_once()
        again = input("Play again? (y/n): ").strip().lower()
        if again not in {"y","yes"}:
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nBye!")
