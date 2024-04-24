import random 
random_number=int(random.randint(1,20))
play=0 
while True:
    guess=int(input("What is your guess?" )) 
    play+=1 
    if guess == random_number: 
        print(f"Congrats! The number was {random_number} \n") 
        break
    elif guess < random_number: 
        print("Guess again, your number is too small! \n")
    elif guess > random_number: 
        print("Guess again, your number is too large! \n")
print(f"You needed {play} guesses to find the correct number.")    