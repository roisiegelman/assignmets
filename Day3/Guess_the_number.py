import random

# Generate a random number between 1-20
def generate_random_number(): 
 return int(random.randint(1,20))

#Get a message for the otions of the game
def player_options():
    return input("Guess the number between 1 and 20, or press 'x' to exit, 'n' for a new game, 's' to show the number): ")

# play the game
def play_game():
    number_to_guess = generate_random_number()
    play = 0 
    
    while True:
     my_input = player_options()
        
     if my_input == 'x':
            print("Exiting the program.")
            return False
     elif my_input == 'n':
            print("Starting a new game.")
            return True
     elif my_input == 's':
            print("The hidden number is:", number_to_guess)
            continue
        
     try:
            my_guess = int(my_input)
     except ValueError:
            print("Invalid input. Please enter a number between 1 and 20.")
            continue
        
     play += 1
     
    
     if my_guess == number_to_guess: 
          print("Congrats! You guessed the number {} correctly in {} guesses.".format(number_to_guess, play))
          return True
        
     elif my_guess < number_to_guess:
          print("Guess again, your number is too small!.")
        
     elif my_guess > number_to_guess:
          print("Guess again, your number is too large!.")

def main():
    print("Welcome to the Number Guessing Game!")
    
    while True:
        if not play_game():
            break
        
        play_again = input("Do you want to play again? (yes/no): ").lower()
        if play_again == 'no':
            print("Exiting the program.")
            break

main()
