import random

# Predefined list of 5 words
WORDS = [
    'python',
    'hangman',
    'computer',
    'programming',
    'keyboard'

]

def choose_word():
    """Select a random word from the list."""
    return random.choice(WORDS).upper()

def display_hangman(incorrect_guesses):
    """Display the hangman figure based on incorrect guesses."""
    stages = [
        """
           -----
           |   |
               |
               |
               |
               |
        =========
        """,
        """
           -----
           |   |
           O   |
               |
               |
               |
        =========
        """,
        """
           -----
           |   |
           O   |
           |   |
               |
               |
        =========
        """,
        """
           -----
           |   |
           O   |
          /|   |
               |
               |
        =========
        """,
        """
           -----
           |   |
           O   |
          /|\\  |
               |
               |
        =========
        """,
        """
           -----
           |   |
           O   |
          /|\\  |
          /    |
               |
        =========
        """,
        """
           -----
           |   |
           O   |
          /|\\  |
          / \\  |
               |
        =========
        """
    ]
    print(stages[incorrect_guesses])

def get_guessed_word(word, guessed_letters):
    """Create the displayed word with guessed letters revealed."""
    return ' '.join([letter if letter in guessed_letters else '_' for letter in word])

def play_hangman():
    print("Welcome to Hangman!")
    print("Guess the word one letter at a time. You have 6 incorrect guesses.")

    word = choose_word()
    guessed_letters = set()
    incorrect_guesses = 0
    max_incorrect = 6

    while incorrect_guesses < max_incorrect:
        display_hangman(incorrect_guesses)
        current_word = get_guessed_word(word, guessed_letters)
        print(f"Word: {current_word}")
        print(f"Guessed letters: {' '.join(sorted(guessed_letters))}")

        if '_' not in current_word:
            print(f"Congratulations! You guessed the word: {word}")
            return

        guess = input("Enter a letter: ").upper().strip()
        if len(guess) != 1 or not guess.isalpha():
            print("Please enter a single letter.")
            continue

        if guess in guessed_letters:
            print("You already guessed that letter.")
            continue

        guessed_letters.add(guess)

        if guess not in word:
            incorrect_guesses += 1
            print(f"Incorrect guess! {max_incorrect - incorrect_guesses} incorrect guesses left.")
        else:
            print("Good guess!")

    display_hangman(incorrect_guesses)
    print(f"Game over! The word was: {word}")

if __name__ == "__main__":
    play_hangman()

