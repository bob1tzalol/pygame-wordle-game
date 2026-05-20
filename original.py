import random

#Variables
max_attempts = 6
current_attempt = 0

WORD_LIST = [
    "birch", "cedar", "roots", "grove", "glade",
    "trail", "brush", "vines", "resin", "acorn",
    "brook", "creek", "shade", "earth", "humus"
]

WORD_LENGTH = 5

GREEN  = '\033[92m'
YELLOW = '\033[93m'
GREY   = '\033[90m'
RESET  = '\033[0m'

#Fonctions
def user_input():
    while True:
        guess = input('Enter your guess: ').strip().lower()
        if len(guess) == WORD_LENGTH and guess.isalpha():
            return guess
        print(f'Please enter a {WORD_LENGTH}-letter word.')


def get_secret_word():
    return random.choice(WORD_LIST)


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


def display_guess_result(guess, result):
    row = []
    for i in range(WORD_LENGTH):
        letter = guess[i].upper()
        if result[i] == 'correct':
            row.append(f'{GREEN} {letter} {RESET}')
        elif result[i] == 'present':
            row.append(f'{YELLOW}[{letter}]{RESET}')
        else:
            row.append(f'{GREY} {letter} {RESET}')
    print('  ' + ' '.join(row))


# Code de jeu principal
while True:
    print('\n' + '=' * 35)
    print('       Welcome to Wordle!')
    print('=' * 35)
    print(f'Guess the {WORD_LENGTH}-letter forest word in {max_attempts} tries.')
    print(f' {GREEN}Correct position:      A  (green){RESET}')
    print(f' {YELLOW}In word, wrong spot: [A] (yellow){RESET}')
    print(f' {GREY}Not in word:           A  (grey){RESET}')
    print('=' * 35 + '\n')

    secret_word = get_secret_word()
    current_attempt = 0
    guesses_log = []

    while current_attempt < max_attempts:
        attempts_left = max_attempts - current_attempt
        print(f'Attempt {current_attempt + 1}/{max_attempts}  ({attempts_left} remaining)')

        guess = user_input()
        result = check_guess(guess, secret_word)
        guesses_log.append((guess, result))

        print()
        print('--- Guesses so far ---')
        for past_guess, past_result in guesses_log:
            display_guess_result(past_guess, past_result)
        print('----------------------')

        if guess == secret_word:
            print(f'\nYou got it in {current_attempt + 1} attempt(s)! The word was: {secret_word.upper()}')
            break

        current_attempt += 1

    else:
        print(f'\nOut of attempts! The word was: {secret_word.upper()}')

    again = input('\nPlay again? (yes/no): ').strip().lower()
    if again not in ('yes', 'y'):
        print('Thanks for playing!')
        break