import random
import time


# Variables
max_attempts = 6
WORD_LENGTH = 5

# Themes
THEMES = {
    "forest": {
        "words": ["birch", "cedar", "roots", "grove", "glade", "trail", "brush", "vines", "resin", "acorn"],
        "color_correct": '\033[92m',  # green
    },
    "ocean": {
        "words": ["coral", "waves", "tides", "shark", "whale", "salty", "beach", "depth", "kelps", "squid"],
        "color_correct": '\033[96m',  # cyan
    },
    "fire": {
        "words": ["flame", "ember", "smoke", "blaze", "burnt", "spark", "ashes", "enfer", "glare"],
        "color_correct": '\033[91m',  # red
    }
}

YELLOW = '\033[93m'
GREY   = '\033[90m'
RESET  = '\033[0m'


# FONCTIONS
def choose_theme():
    while True:
        choice = input("Choose theme (forest/ocean/fire): ").strip().lower()
        if choice in THEMES:
            return choice
        print("Invalid choice. Try again.")

def choose_mode():
    print("\nChoose a game mode:")
    print("1. Normal")
    print("2. Time Attack (60 seconds)")

    while True:
        choice = input("Enter choice: ")
        if choice == '1':
            return "normal"
        elif choice == '2':
            return "time"
        print("Invalid choice.")

def user_input():
    while True:
        guess = input('Enter your guess: ').strip().lower()
        if len(guess) == WORD_LENGTH and guess.isalpha():
            return guess
        print(f'Please enter a {WORD_LENGTH}-letter word.')

def get_secret_word(word_list):
    return random.choice(word_list)

def check_guess(guess, secret):
    result = ['absent'] * WORD_LENGTH
    secret_remaining = list(secret)
    guess_remaining = list(guess)

    for i in range(WORD_LENGTH):
        if guess[i] == secret[i]:
            result[i] = 'correct'
            secret_remaining[i] = None
            guess_remaining[i] = None

    for i in range(WORD_LENGTH):
        if guess_remaining[i] is not None:
            if guess_remaining[i] in secret_remaining:
                result[i] = 'present'
                secret_remaining[secret_remaining.index(guess_remaining[i])] = None

    return result

def display_guess_result(guess, result, correct_color):
    row = []
    for i in range(WORD_LENGTH):
        letter = guess[i].upper()
        if result[i] == 'correct':
            row.append(f'{correct_color} {letter} {RESET}')
        elif result[i] == 'present':
            row.append(f'{YELLOW}[{letter}]{RESET}')
        else:
            row.append(f'{GREY} {letter} {RESET}')
    print('  ' + ' '.join(row))

def give_hint(secret, guesses_log):
    known_letters = set()

    for guess, result in guesses_log:
        for i in range(len(guess)):
            if result[i] in ("correct", "present"):
                known_letters.add(guess[i])

    remaining_letters = [letter for letter in secret if letter not in known_letters]

    if not remaining_letters:
        return None

    return random.choice(remaining_letters)


# CODE DE JEU
while True:
    print('\n' + '=' * 35)
    print('       Welcome to Wordle!')
    print('=' * 35)

    theme_name = choose_theme()
    mode = choose_mode()

    theme = THEMES[theme_name]
    word_list = theme["words"]
    COLOR = theme["color_correct"]

    print(f"\nTheme: {theme_name.capitalize()}")
    print(f"Mode: {mode.capitalize()}")
    print('=' * 35 + '\n')

    secret_word = get_secret_word(word_list)
    current_attempt = 0
    guesses_log = []
    revealed_positions = set()

    start_time = time.time()

    while current_attempt < max_attempts:
        # TIME ATTACK
        if mode == "time":
            if time.time() - start_time > 60:
                print("\nTime's up!")
                break
            print(f"Time left: {int(60 - (time.time() - start_time))}s")

        print(f'\nAttempt {current_attempt + 1}/{max_attempts}')

        # HINT
        if current_attempt >= 3:
            use_hint = input("Type 'hint' for a hint or press Enter: ").lower()

            if use_hint == "hint":
                hint = give_hint(secret_word, guesses_log)

                if hint:
                    print(f"Hint: The word contains the letter '{hint.upper()}'")
                else:
                    print("No more useful hints available.")

        guess = user_input()
        result = check_guess(guess, secret_word)
        guesses_log.append((guess, result))

        print('\n--- Guesses so far ---')
        for past_guess, past_result in guesses_log:
            display_guess_result(past_guess, past_result, GREEN)
        print('----------------------')


        if guess == secret_word:
            print(f'\nYou got it! The word was: {secret_word.upper()}')
            break

        current_attempt += 1

    else:
        print(f'\nOut of attempts! The word was: {secret_word.upper()}')

    again = input('\nPlay again? (yes/no): ').strip().lower()
    if again not in ('yes', 'y'):
        print('Thanks for playing!')
        break