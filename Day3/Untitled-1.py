import random

def generate_random_number():
    return random.randint(1, 20)

def get_user_guess():
    return input("Guess the number between 1 and 20 (or 'x' to exit, 'n' for a new game, 's' to show the number): ")

def play_game():
    number_to_guess = generate_random_number()
    guesses = 0

    while True:
        user_input = get_user_guess()

        if user_input == 'x':
            print("Exiting the program.")
            return False
        elif user_input == 'n':
            print("Starting a new game.")
            return True
        elif user_input == 's':
            print("The hidden number is:", number_to_guess)
            continue

        try:
            user_guess = int(user_input)
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 20.")
            continue

        guesses += 1

        if user_guess == number_to_guess:
            print("Congratulations! You guessed the number {} correctly in {} guesses.".format(number_to_guess, guesses))
            return True
        elif user_guess < number_to_guess:
            print("Too small! Try again.")
        else:
            print("Too big! Try again.")
print(f"You needed {guesses} guesses to find the correct number.")    
def main():
    while True:
        if not play_game():
            break
        play_again = input("Do you want to play again? (yes/no): ").lower()
        while play_again not in ['yes', 'no']:
            print("Invalid input. Please enter 'yes' or 'no'.")
            play_again = input("Do you want to play again? (yes/no): ").lower()
        if play_again == 'no':
            print("Exiting the program.")
            break