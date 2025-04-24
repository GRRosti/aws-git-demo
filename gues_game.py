import random

def play_guessing_game():
    """Plays a single round of the number guessing game."""
    random_number = random.randint(1, 20)
    attempts = 0
    max_attempts = 5

    print("I'm thinking of a number between 1 and 20.")

    while attempts < max_attempts:
        try:
            guess = int(input("Enter your guess: "))
            attempts += 1

            if guess < random_number:
                print("Too low!")
            elif guess > random_number:
                print("Too high!")
            else:
                print(f"Correct! You guessed it in {attempts} attempts!")
                return True  # User guessed correctly, return True to indicate a win

        except ValueError:
            print("Invalid input. Please enter an integer.")

    # If the loop finishes without a correct guess
    print(f"Game over! You ran out of attempts.")
    print(f"The correct number was {random_number}.")
    return False # User failed to guess, return False to indicate a loss

# Main game loop for multiple rounds
while True:
    play_guessing_game()

    while True:
        play_again = input("Do you want to play again? (yes/no): ").lower()
        if play_again in ['yes', 'y', 'no', 'n']:
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

    if play_again in ['no', 'n']:
        print("Thanks for playing!")
        break