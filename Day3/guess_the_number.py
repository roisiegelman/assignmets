
import random

def generate_random_number():
    return int(random.randint(1,20))

def welcome_to_game():
    return input("Guess the number between 1 and 20 or 'x' to exit, 'n' for a new game or 's' to show the number ")

def play_game():
    random_number = generate_random_number()
    play = 0

    while True:
        my_guess = welcome_to_game()

        if my_guess == 'x':
            print("Exiting the program.")
            return False
        elif my_guess == 'n':
            print("Starting a new game.")
            return True
        elif my_guess == 's':
            print("The hidden number is:", random_number)
            continue

        try:
            my_guess = int(my_guess)
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 20.")
            continue

        play += 1

        if my_guess == random_number:
            print("congrats!  The number was {}. You needed {} guesses to find the correct number .".format(random_number, play))
            return True
        elif my_guess < random_number:
            print("Too small! Try again.")
        else:
            print("Too big! Try again.")

def main():
    while True:
        if not play_game():
            break
        play_again = input("Do you want to play again? (yes/no): ").lower()
        while play_again not in ['yes', 'no']:
            print("Invalid input. Please enter 'yes' or 'no'.")
            play_again = input("Do you want to play again? (yes/no): ").lower()
        if play_again == 'no':
            print("Goodbye.")
            break

if __name__ == "__main__":
    main()
