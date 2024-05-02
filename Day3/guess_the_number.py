import random

def generate_random_number():
    return random.randint(1, 20)

def get_user_guess():
    return input("Guess the number between 1 and 20 or 'x' to exit, 'n' for a new game or 's' to show the number ")

def play_game():
    random_number = generate_random_number()
    play = 0

    while True:
        user_input = get_user_guess()

        if user_input == 'x':
            print("Exiting the program.")
            return False
        elif user_input == 'n':
            print("Starting a new game.")
            return True
        elif user_input == 's':
            print("The hidden number is:", random_number)
            continue

        try:
            user_guess = int(user_input)
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 20.")
            continue

        play += 1

        if user_guess == random_number:
            print("congrats! Congrats! The number was {}. You needed {} guesses to find the correct number .".format(random_number, play))
            return True
        elif user_guess < random_number:
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
